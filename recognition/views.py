# -*- coding: utf-8 -*-

# Create your views here.
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from django.shortcuts import render
import os
import simplejson
import uuid
import zipfile
from InsMaster import settings
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from io import open

import tensorflow as tf
import librosa
import numpy as np
import ctypes.util

from magenta.common import tf_utils
from magenta.music import audio_io
from magenta.music import sequences_lib
import magenta.music as mm
from magenta.models.onsets_frames_transcription import configs
from magenta.models.onsets_frames_transcription import constants
from magenta.models.onsets_frames_transcription import data
from magenta.models.onsets_frames_transcription import split_audio_and_label_data
from magenta.models.onsets_frames_transcription import train_util
from magenta.music import midi_io
from magenta.protobuf import music_pb2

# Create your views here.

uploaded_file_local_path = None


@csrf_exempt
def uploadifive_script(request):
    ret = u"0"
    file = request.FILES.get(u"Filedata", None)
    if file:
        result, new_name = profile_upload(file)
        if result:
            ret = u"1"
        else:
            ret = u"2"
        json = {u'ret': ret, u'save_name': new_name}
    else:
        json = {u'ret': ret, u'save_name': u'null'}
    return HttpResponse(simplejson.dumps(json, ensure_ascii=False))

@csrf_exempt
def profile_upload(file):
    global uploaded_file_local_path
    if file:
        path = os.path.join(os.getcwdu(), u'static/files/recognition')
        wav_path=path+'/wav'
        file_name = unicode(uuid.uuid1()) + u'-' + file.name
        path_file = os.path.join(wav_path, file_name)
        fp = open(path_file, u'wb')
        for content in file.chunks():
            fp.write(content)
        fp.close()


        #music transcription

        #get necessary
        CHECKPOINT_DIR = os.path.join(os.getcwdu(),'model')

        acoustic_checkpoint = tf.train.latest_checkpoint(CHECKPOINT_DIR)
        print('acoustic_checkpoint=' + acoustic_checkpoint)

        filename = path_file
        content = open(filename, 'rb')
        uploaded = {filename: content.read()}  ##todo
        #end

        # model initialization
        config = configs.CONFIG_MAP['onsets_frames']
        hparams = config.hparams
        hparams.use_cudnn = False
        hparams.batch_size = 1

        examples = tf.placeholder(tf.string, [None])

        dataset = data.provide_batch(
            examples=examples,
            preprocess_examples=True,
            hparams=hparams,
            is_training=False)

        estimator = train_util.create_estimator(
            config.model_fn, CHECKPOINT_DIR, hparams)

        iterator = dataset.make_initializable_iterator()
        next_record = iterator.get_next()
        # end

        # preprocess
        to_process = []
        for fn in uploaded.keys():
            print('User uploaded file "{name}" with length {length} bytes'.format(
                name=fn, length=len(uploaded[fn])))
            wav_data = uploaded[fn]
            example_list = list(
                split_audio_and_label_data.process_record(
                    wav_data=wav_data,
                    ns=music_pb2.NoteSequence(),
                    example_id=fn,
                    min_length=0,
                    max_length=-1,
                    allow_empty_notesequence=True))
            assert len(example_list) == 1
            to_process.append(example_list[0].SerializeToString())
            print('Processing complete for', fn)

        sess = tf.Session()

        sess.run([
            tf.initializers.global_variables(),
            tf.initializers.local_variables()
        ])

        sess.run(iterator.initializer, {examples: to_process})

        def input_fn(params):
            del params
            return tf.data.Dataset.from_tensors(sess.run(next_record))
        # end

        # inference
        prediction_list = list(
            estimator.predict(
                input_fn,
                yield_single_examples=False))
        assert len(prediction_list) == 1

        frame_predictions = prediction_list[0]['frame_probs_flat'] > .5
        onset_predictions = prediction_list[0]['onset_probs_flat'] > .5
        velocity_values = prediction_list[0]['velocity_values_flat']

        sequence_prediction = sequences_lib.pianoroll_to_note_sequence(
            frame_predictions,
            frames_per_second=data.hparams_frames_per_second(hparams),
            min_duration_ms=0,
            min_midi_pitch=constants.MIN_MIDI_PITCH,
            onset_predictions=onset_predictions,
            velocity_values=velocity_values)

        # Ignore warnings caused by pyfluidsynth
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        mm.plot_sequence(sequence_prediction)
        mm.play_sequence(sequence_prediction, mm.midi_synth.fluidsynth,
                         colab_ephemeral=False)
        # end

        midi_filename = (file_name+ '.mid').replace(' ', '_')
        midi_path = path + u'/midi/' + midi_filename


        midi_io.sequence_proto_to_midi_file(sequence=sequence_prediction, output_file=midi_path)

        #end

        uploaded_file_local_path = midi_path

        #os.system(u'sheet.exe '+ path + u'/' + file_name +  u' ' + path + u'/' + file.name)
        #os.system(
        #    u'wine /home/wangsongyi/InsMaster/PlayItYourself_web\ /sheet.exe '
        #    + path + u'/' + file_name + u' ' + path + u'/' + file.name
        #)
        png_dir = path + '/png/'
        ly_dir  = path + '/ly/'
        pdf_dir = path + '/pdf/'
        ly_path = ly_dir + file_name + '.ly'
        pdf_name= file_name+'.pdf'
        pdf_path= pdf_dir+ file_name + '.pdf'
        os.system(u'midi2ly --output=' + ly_path + ' ' + midi_path)
        os.system(u'lilypond --pdf --output=' + pdf_path + ' ' + ly_path)

        fzip = zipfile.ZipFile(path + u'/zip/' + file.name + u'.zip', u'w', zipfile.ZIP_DEFLATED)

        fzip.write(midi_path,midi_filename)

        fzip.write(pdf_path,pdf_name)

        fzip.close()
        uploaded_file_local_path = path + u'/zip/' + file.name + u'.zip'
        return (True, file.name)
    return (False, u'Error_File_Name')

@csrf_exempt
def profile_delete(request):
    del_file = request.POST.get(u"delete_file", u'')
    if del_file:
        path_file = os.path.join(settings.MEDIA_ROOT, u'upload', del_file)
        os.remove(path_file)

@csrf_exempt
def download(request):
    global uploaded_file_local_path

    if uploaded_file_local_path is None:
        return HttpResponse(u"<p>No MIDI files for download.</p>")
    file_name = uploaded_file_local_path

    def read_file(file_name, buf_size = 25536):
        f = open(file_name, u'rb')
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()
    response = StreamingHttpResponse(read_file(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response
