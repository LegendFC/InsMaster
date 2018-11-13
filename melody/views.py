# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
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

# Create your views here.
download_file_local_path = None


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
    global download_file_local_path
    if file:
        path = os.path.join(os.getcwdu(), u'static/files')
        file_name = unicode(uuid.uuid1()) + u'-' + file.name
        midi_path=path+'/midi'
        path_file = os.path.join(midi_path, file_name)
        fp = open(path_file, u'wb')
        for content in file.chunks():
            fp.write(content)
        fp.close()

        # os.system(u'wine /home/wangsongyi/InsMaster/PlayItYourself_web\ /sheet.exe '+ path + u'/' + file_name +  u' ' + path + u'/' + file.name)#call_sheet.exe
        png_dir = path + '/png/'
        ly_path = png_dir + file_name + '.ly'
        os.system(u'midi2ly --output=' + ly_path + ' ' + path_file)
        os.system(u'lilypond --png --output=' + png_dir + file.name + ' ' + ly_path)
        # os.system(u'lilypond --png --output='+file_name+' '+)

        fzip = zipfile.ZipFile(path + u'/png/' + file.name + u'.zip', u'w', zipfile.ZIP_DEFLATED)
        curNum = 1
        curFile = path + u'/png/' + file.name + u'-page' + unicode(curNum) + u'.png'
        while (os.path.exists(curFile)):
            fzip.write(curFile)
            curNum = curNum + 1
            curFile = path + u'/png/' + file.name + u'-page' + unicode(curNum) + u'.png'
        fzip.close()
        download_file_local_path = path + u'/png/' + file.name + u'.zip'
        return (True, file.name)
    return (False, u'Error_File_Name')


@csrf_exempt
def profile_delete(request):
    del_file = request.POST.get(u"delete_file", u'')
    if del_file:
        path_file = os.path.join(settings.MEDIA_ROOT, u'upload', del_file)
        os.remove(path_file)
        # wav  #png


@csrf_exempt
def download(request):
    global download_file_local_path
    if download_file_local_path is None:
        return HttpResponse(u"<p>No MIDI files for download.</p>")

    # path = os.path.join(os.getcwdu(), u'index/static/upload')
    # file_name = path + u'/' + file
    file_name = download_file_local_path

    def read_file(file_name, buf_size=25536):
        f = open(file_name, u'rb')
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    response = HttpResponse(read_file(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response