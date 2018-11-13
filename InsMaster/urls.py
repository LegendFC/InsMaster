"""InsMaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
# from recognition.views import uploadify_script as uploadify_script1
from melody.views import uploadifive_script as melody_upload
# from recognition.views import download as download1
from melody.views import download as melody_download


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name=u'index.html')),
    url(r'^index/$', TemplateView.as_view(template_name=u'index.html')),
    url(r'^recognition/$', TemplateView.as_view(template_name=u'recognition.html')),
    url(r'^melody/$', TemplateView.as_view(template_name=u'melody.html')),
    url(r'^chord/$', TemplateView.as_view(template_name=u'chord.html')),
    url(r'^help/$', TemplateView.as_view(template_name=u'help.html')),
    url(r'^about/$', TemplateView.as_view(template_name=u'about.html')),

    url(r'^melody/upload/$',melody_upload),
    url(r'^melody/download/$',melody_download)
]
