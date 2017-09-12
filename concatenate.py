# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 17:27:48 2017

@author: Utilisateur
"""

import cv2
from moviepy.editor import *


def concatenate(videofiles) :
    video_index = 0
    cap = cv2.VideoCapture(videofiles[0])
    
    # video resolution: 1624x1234 px
    out = cv2.VideoWriter("video.mp4", 
                          cv2.VideoWriter_fourcc(*'MP4V'), 
                          30, (1920, 1080), 1)
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if frame is None:
            print ("end of video " + str(video_index) + " .. next one now")
            video_index += 1
            if video_index >= len(videofiles):
                break
            cap = cv2.VideoCapture(videofiles[ video_index ])
            ret, frame = cap.read()
        cv2.imshow('frame',frame)
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print( "end.")
    return

def concatenate2(videofiles, outputName="videoFinale.mp4") :
    
    clip=[]
    for video in videofiles :
        print("1")
        clip.append(VideoFileClip(video, audio=True))
    final_clip= concatenate_videoclips(clip, method="compose")
    final_clip.write_videofile(outputName)
    return 
        