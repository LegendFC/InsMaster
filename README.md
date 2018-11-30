# InsMaster

## Introduction

**InsMaster** is an artificial intelligence which provides free music scores for musicians and amateurs by automatic music transcription. Once you have an audio file, you can get its music score by using this app. 

**InsMaster** is a Django Web APP for AMT(automatic music transcription) . Deep neural networks are used to cover the transcription work. Through the Django APP, you can convert your audio files (wav,mp3 ,aac,ogg etc)  into midi files. Additionaly, you can convert your midi files into music sheet with image(png)  files. It gets the best performance for pure piano music.

The  project is bulit with python2.7.

## Getting Started

You can try our app on  [our website](140.143.208.38:8010). If it is not available, you can contact us at once. Or, you can build the environment for the project in your own machine to test it.

## Installation

Ubuntu is recommended for this project. If you use other systems, the insturctions below may not work.

### software installation

**Requirements:**`python==2.7`

You can use `apt-get install` or other commands to install the software below.

`libasound-dev`
`libjack-dev`
`ffmpeg`

### python packages

Use `pip install` to get python packages.

`django==1.11`

`tensorflow` or `tensorflow-gpu`

`simplejson`

`librosa`

`setuptools==39.0.1`

`magenta==0.3.19` or `magenta-gpu==0.3.19`

### other ways to build the project

You can use a docker to finish all these installations if you are familar with it. It is much easier and more flexible. Or you can create a virtual python environment to do part of the installation.

## Using InsMaster

### Start

In the project directory, use `python manage.py runserver IP:Port` to run the django server.

### Use

Now use the browser to use it.

![](E:\experience\InsMaster\InsMaster\图片\luping.gif)

![](E:\experience\InsMaster\InsMaster\图片\1.png)


