# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import os
import shutil
import subprocess
from moviepy.editor import VideoFileClip
from mutagen.mp3 import MP3
import wave
import contextlib

def extractionVideosExtractsAndSounds(videoName, width, freq, formatOutputSound) :
    """
    this function extracts sounds of 2*width seconds from a video and the 2*width videoExtract without sound associated with
    """
    
    V=VideoFileClip(videoName)
    duration = (V.duration)

    if os.path.isfile(videoName[:-4]+"son") :
        os.rename(videoName[:-4]+"son", videoName[:-4]+"son"+"renamed")
    if (os.path.isdir(videoName[:-4]+"son") is False):
        os.mkdir(videoName[:-4]+"son")
    else :
        shutil.rmtree(videoName[:-4]+"son") #erase a directory
        os.mkdir(videoName[:-4]+"son")
     
    if os.path.isfile(videoName[:-4]+"vid") :
        os.rename(videoName[:-4]+"son", videoName[:-4]+"vid"+"renamed")
    if (os.path.isdir(videoName[:-4]+"vid") is False):
        os.mkdir(videoName[:-4]+"vid")
    else :
        shutil.rmtree(videoName[:-4]+"vid") #erase a directory
        os.mkdir(videoName[:-4]+"vid")
    compt=1
    startTime=freq-int(2*width)
    while (startTime<0):
        print("impossible to start before the beginning of the video")
        startTime+=freq

    while(startTime+int(2*width)<duration):
        startTimeH,startTimeMin, startTimeSec=convSecToHMinSec(startTime)
        print("beforeif")
        if (os.path.isfile("extract.mp4") is True):
            print("true")
            os.remove("extract.mp4")
            
        extractSoundName=videoName[:-4]+"son"+"/"+"sound"+str(compt)+"."+str(formatOutputSound)
        extractVidName=videoName[:-4]+"vid"+"/"+"vid"+str(compt)+"."+"mp4"

        
        #print(extractSoundName)
        ##command = 'ffmpeg -i '+videoName+" -ss "+str(startTimeH)+":"+str(startTimeMin)+":"+str(startTimeSec)+".00"+" -t 00:00:"+str(int(2*width))+".00 -c:v copy -c:a copy  "+"extract.mp4" #cree l'extrait video qui nous interesse
        command = 'ffmpeg -i '+videoName+" -ss "+str(startTimeH)+":"+str(startTimeMin)+":"+str(startTimeSec)+".00"+" -t 00:00:"+str(int(2*width))+".00 "+"-async 1 -strict 2 extract.mp4" #cree l'extrait video qui nous interesse
        #command = 'ffmpeg -i '+videoName+" -ss 00:1:45.00 -t 00:00:30.00 -c:v copy -c:a copy  extrait2.mp4"
        subprocess.call(command, shell=True)

        print(extractVidName)

        print(extractSoundName)
        #command = 'ffmpeg -i '+videoName+" -ss "+str(startTimeH)+":"+str(startTimeMin)+":"+str(startTimeSec)+".00"+" -t 00:00:"+str(int(2*width))+".00 -c:v copy -c:a copy  "+"extract.mp4" #cree l'extrait video qui nous interesse
        #command = 'ffmpeg -i '+videoName+" -ss 00:1:45.00 -t 00:00:30.00 -c:v copy -c:a copy  extrait2.mp4"
        #subprocess.call(command, shell=True)

        command = 'ffmpeg -i '+'extract.mp4 '+'-c copy -an '+extractVidName
        subprocess.call(command, shell=True)
        command="ffmpeg -i "+"extract.mp4"+" "+extractSoundName
        subprocess.call(command, shell=True)
        startTime+=freq
        compt+=1


    return

def extractionImagesV2(videoName, formatOutput, width, freq, notTaken=0, nb=float('inf')) :
    """
    this function extracts the images from a video
    """
    if os.path.isfile(videoName[:-4]) :
        os.rename(videoName[:-4], videoName[:-4]+"renamed")
    if (os.path.isdir(videoName[:-4]) is False):
        os.mkdir(videoName[:-4])
    else :
        shutil.rmtree(videoName[:-4]) #erase a directory
        os.mkdir(videoName[:-4])
    print("ici") 
    compt=0
    stop=0
    V=VideoFileClip(videoName)
    duration=V.duration
    compt+=1
    next=width+freq*(notTaken)
    while (stop==0 and compt<=nb) :       
        if(next<=duration) :
         
            imName=videoName[:-4]+"/"+"im"+str(compt)+"."+str(formatOutput)
            print("bool", imName, next)
            if os.path.isfile(imName) :
                os.remove(imName)
            V.save_frame(imName, next)
            compt+=1
            next+=freq
            print(next)
        else :
            stop=1
    return 


def extractionSons(videoName, duration, formatOutputSound, width, freq) :
    """
    this function extracts sounds of 2*width seconds from a video
    it returns th nb of sounds extracted and the number of extracts not taken at the beginning of the video (useful in the case of width>freq)
    """
    if os.path.isfile(videoName[:-4]+"son") :
        os.rename(videoName[:-4]+"son", videoName[:-4]+"son"+"renamed")
    if (os.path.isdir(videoName[:-4]+"son") is False):
        os.mkdir(videoName[:-4]+"son")
    else :
        shutil.rmtree(videoName[:-4]+"son") #erase a directory
        os.mkdir(videoName[:-4]+"son")
        
    compt=1
    startTime=freq-int(2*width)
    notTaken=0
    while (startTime<0):
        print("impossible to start before the beginning of the video")
        startTime+=freq
        notTaken+=1
    while(startTime+int(2*width)<duration):
        startTimeH,startTimeMin, startTimeSec=convSecToHMinSec(startTime)

        if (os.path.isfile("extract.mp4") is True):
            os.remove("extract.mp4")

        extractSoundName=videoName[:-4]+"son"+"/"+"sound"+str(compt)+"."+str(formatOutputSound)
        print(extractSoundName)
        command = 'ffmpeg -i '+videoName+" -ss "+str(startTimeH)+":"+str(startTimeMin)+":"+str(startTimeSec)+".00"+" -t 00:00:"+str(int(2*width))+".00 -c:v copy -c:a copy  "+"extract.mp4" #cree l'extrait video qui nous interesse
        #command = 'ffmpeg -i '+videoName+" -ss 00:1:45.00 -t 00:00:30.00 -c:v copy -c:a copy  extrait2.mp4"
        subprocess.call(command, shell=True)
        command="ffmpeg -i "+"extract.mp4"+" "+extractSoundName
        subprocess.call(command, shell=True)
        startTime+=freq
        compt+=1

    return notTaken, compt-1

def convSecToHMinSec(startTime) :
    """
    startTime is in seconds
    """
    H=startTime//3600
    startTime-=H*3600
    minutes = startTime//60
    startTime-=minutes*60
    sec= startTime
    
    return H, minutes, sec

"""
video.set(propId, value)
video.get(property_id)
0CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds or video capture timestamp.
1CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
5CV_CAP_PROP_FPS Frame rate.
7CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
"""


def extractionImagesAndSounds(videoName, formatOutput, formatOutputSound, width, freq):
    """
    combination of the two functions above
    """
    V=VideoFileClip(videoName)
    duration = (V.duration)
    notTaken, nb = extractionSons(videoName, duration, formatOutputSound, width, freq)
    print(nb)
    print(notTaken)
    extractionImagesV2(videoName, formatOutput, width, freq, notTaken, nb)
    return 




def JustSoundsExtracts(videoName, formatOutputSound, width, freq):
    """
    this functions does the extraction of 2*width seconds sounds from a music or a video without taking care of the presence of images if it is a video
    """
    
    if videoName[-3:] == 'mp3' :
        
        audio = MP3(videoName)
        duration=audio.info.length
        extractionSonsFromMusic(videoName, duration, formatOutputSound, width, freq)
    elif videoName[-3:] == 'wav' :
        with contextlib.closing(wave.open(videoName,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        extractionSonsFromMusic(videoName, duration, formatOutputSound, width, freq)
    elif videoName[-3:] == 'mp4' :
            V=VideoFileClip(videoName)
            duration = (V.duration)
           
            notTaken, nb = extractionSons(videoName, duration, formatOutputSound, width, freq)
    return

def extractionSonsFromMusic(musicName, duration, formatOutputSound, width, freq) :
    """
    extracts sounds of 2*width seconds from a music but does not work with a mp4 format
    """
    if os.path.isfile(musicName[:-4]+"son") :
        os.rename(musicName[:-4]+"son", musicName[:-4]++"son_"+"renamed")
    if (os.path.isdir(musicName[:-4]+"son") is False):
        os.mkdir(musicName[:-4]+"son")
    else :
        shutil.rmtree(musicName[:-4]+"son") #erase a directory
        os.mkdir(musicName[:-4]+"son")
        
    compt=1
    startTime=freq-int(2*width)
    notTaken=0
    while (startTime<0):
        startTime+=freq
        notTaken+=1
    while(startTime+int(2*width)<duration):
        startTimeH,startTimeMin, startTimeSec=convSecToHMinSec(startTime)
        extractSoundName=musicName[:-4]+"son"+"/"+"sound"+str(compt)+"."+str(formatOutputSound)
        command="ffmpeg -ss "+str(startTimeH)+":"+str(startTimeMin)+":"+str(startTimeSec)+".00"+" -t "+"00:00:"+str(int(2*width))+".00"+" -i "+musicName+" "+extractSoundName
        subprocess.call(command, shell=True)
        startTime+=freq
        compt+=1

    return 
    

