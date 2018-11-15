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
import magenta.music as mm
from magenta.models.onsets_frames_transcription import model
from magenta.models.onsets_frames_transcription import constants
from magenta.models.onsets_frames_transcription import data
from magenta.models.onsets_frames_transcription import infer_util
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
        path = os.path.join(os.getcwdu(), u'static/files')
        wav_path=path+'/wav'
        file_name = unicode(uuid.uuid1()) + u'-' + file.name
        path_file = os.path.join(wav_path, file_name)
        fp = open(path_file, u'wb')
        for content in file.chunks():
            fp.write(content)
        fp.close()



        orig_find_library = ctypes.util.find_library

        def proxy_find_library(lib):
            if lib == 'fluidsynth':
                return 'libfluidsynth.so.1'
            else:
                return orig_find_library(lib)

        ctypes.util.find_library = proxy_find_library

        CHECKPOINT_DIR = '../model'  ##todo

        acoustic_checkpoint = tf.train.latest_checkpoint(CHECKPOINT_DIR)
        print('acoustic_checkpoint=' + str(acoustic_checkpoint))
        hparams = tf_utils.merge_hparams(
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

        filename = path_file
        # file_dir = './index/static/upload/' + filename
        content = open(filename, 'rb')
        uploaded = {filename: content.read()}  ##todo

        to_process = []
        for fn in uploaded.keys():
            print('User uploaded file "{name}" with length {length} bytes'.format(
                name=fn, length=len(uploaded[fn])))
            open(fn, 'wb').write(uploaded[fn])
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

        midi_filename = (filenames[0] + '.mid').replace(' ', '_')
        midi_filename = path + u'/midi' + midi_filename[midi_filename.find('upload') + 6:]
        uploaded_file_local_path = midi_filename
        #os.system('touch /home/wangsongyi/InsMaster/PlayItYourself_web\ /index/static/upload/midi/xinjing.wav.mid')
        #f = open(midi_filename, 'w')
        #f.close()
        midi_io.sequence_proto_to_midi_file(sequence=sequence_prediction, output_file=midi_filename)

        #os.system(u'sheet.exe '+ path + u'/' + file_name +  u' ' + path + u'/' + file.name)
        #os.system(
        #    u'wine /home/wangsongyi/InsMaster/PlayItYourself_web\ /sheet.exe '
        #    + path + u'/' + file_name + u' ' + path + u'/' + file.name
        #)
        png_dir = path + '/png/'
        ly_path = png_dir + file_name + '.ly'
        os.system(u'midi2ly --output=' + ly_path + ' ' + midi_filename)
        os.system(u'lilypond --png --output=' + png_dir + file.name + ' ' + ly_path)

        fzip = zipfile.ZipFile(path + u'/png/' + file.name + u'.zip', u'w', zipfile.ZIP_DEFLATED)
        curNum = 1
        curFile = path + u'/png/' + file.name + u'-page' + unicode(curNum) + u'.png'
        while (os.path.exists(curFile)):
            fzip.write(curFile)
            curNum = curNum + 1
            curFile = path + u'/png/' + file.name + u'-page' + unicode(curNum) + u'.png'
        fzip.close()
        uploaded_file_local_path = path + u'/png/' + file.name + u'.zip'
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
    path = os.path.join(os.getcwdu(), u'index/static/upload/midi')
    #file_name = path + u'/' + file

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
