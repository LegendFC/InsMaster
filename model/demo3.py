from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import librosa
import numpy as np
import ctypes.util

from magenta.common import tf_utils
from magenta.music import audio_io
import magenta.music as mm
from magenta.models.onsets_frames_transcription import model
from magenta.models.onsets_frames_transcription import constants
from magenta.models.onsets_frames_transcription import data
from magenta.models.onsets_frames_transcription import infer_util
from magenta.music import midi_io
from magenta.protobuf import music_pb2



orig_find_library = ctypes.util.find_library
def proxy_find_library(lib):
  if lib == 'fluidsynth':
    return 'libfluidsynth.so.1'
  else:
    return orig_find_library(lib)

ctypes.util.find_library = proxy_find_library

CHECKPOINT_DIR = './train/train_50002'   ##todo



acoustic_checkpoint = tf.train.latest_checkpoint(CHECKPOINT_DIR)
print('acoustic_checkpoint=' + acoustic_checkpoint)
hparams =  tf_utils.merge_hparams(
      constants.DEFAULT_HPARAMS, model.get_default_hparams())

with tf.Graph().as_default():
  examples = tf.placeholder(tf.string, [None])

  num_dims = constants.MIDI_PITCHES

  batch, iterator = data.provide_batch(
      batch_size=1,
      examples=examples,
      hparams=hparams,
      is_training=False,
      truncated_length=0)

  model.get_model(batch, hparams, is_training=False)

  session = tf.Session()
  saver = tf.train.Saver()
  saver.restore(session, acoustic_checkpoint)

  onset_probs_flat = tf.get_default_graph().get_tensor_by_name(
      'onsets/onset_probs_flat:0')
  frame_probs_flat = tf.get_default_graph().get_tensor_by_name(
     'frame_probs_flat:0')

# file = open('./data/wav_format/xinjing.wav','w')   ##todo
# to_process = []

# wav_data = audio_io.samples_to_wav_data(
#     librosa.util.normalize(librosa.core.load(file, sr=hparams.sample_rate)[0]),
#     hparams.sample_rate)

# example = tf.train.Example(features=tf.train.Features(feature={
#     'id':
#         tf.train.Feature(bytes_list=tf.train.BytesList(
#             value=[file.encode('utf-8')]
#         )),
#     'sequence':
#         tf.train.Feature(bytes_list=tf.train.BytesList(
#             value=[music_pb2.NoteSequence().SerializeToString()]
#         )),
#     'audio':
#         tf.train.Feature(bytes_list=tf.train.BytesList(
#             value=[wav_data]
#         )),
# }))
# to_process.append(example.SerializeToString())
# print('Processing complete ')

filename='richard.wav'
file_dir='./data/wav_format/'+filename
content=open(file_dir,'rb')
uploaded = {file_dir:content.read()}          ##todo

to_process = []
for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))
  open(fn, 'w').write(uploaded[fn])
  wav_data = audio_io.samples_to_wav_data(
      librosa.util.normalize(librosa.core.load(fn, sr=hparams.sample_rate)[0]),
      hparams.sample_rate)

  example = tf.train.Example(features=tf.train.Features(feature={
      'id':
          tf.train.Feature(bytes_list=tf.train.BytesList(
              value=[fn.encode('utf-8')]
          )),
      'sequence':
          tf.train.Feature(bytes_list=tf.train.BytesList(
              value=[music_pb2.NoteSequence().SerializeToString()]
          )),
      'audio':
          tf.train.Feature(bytes_list=tf.train.BytesList(
              value=[wav_data]
          )),
  }))
  to_process.append(example.SerializeToString())
  print('Processing complete for', fn)


session.run(iterator.initializer, {examples: to_process})

filenames, frame_logits, onset_logits = session.run([
    batch.filenames,
    frame_probs_flat,
    onset_probs_flat
])

print('Inference complete for', filenames[0])

frame_predictions = frame_logits > .5

onset_predictions = onset_logits > .5

sequence_prediction = infer_util.pianoroll_to_note_sequence(
    frame_predictions,
    frames_per_second=data.hparams_frames_per_second(hparams),
    min_duration_ms=0,
    onset_predictions=onset_predictions)

midi_filename = (filenames[0] + '.mid').replace(' ', '_')                ##todo
midi_dir = {'./output/'+midi_filename}
midi_io.sequence_proto_to_midi_file(sequence_prediction, midi_filename)