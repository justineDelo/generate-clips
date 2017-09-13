#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 09:57:38 2017

@author: justine
"""

import matplotlib.pyplot as plt
import inception
import os
import generation
import extractionImages
import moviepy.editor as mp 
import shutil
import numpy as np
import features

def featuresImages(path, imagesPaths) :
    """
    this function takes a list of images in parameter 
    It computes a feature vector using inception for each of these images and returns an array with all the features
    """
    images=[]
    for ima in imagesPaths :
        images.append(plt.imread(ima))

    
    out=[]
    c=0
    #image = [cv2.imread("test.png")]       
    inception.maybe_download()
    model = inception.Inception()
    from inception import transfer_values_cache
    for im in images :
        c+=1
        image=[im]
    

        #file_path_cache_train = os.path.join(os.path.expanduser("~"),"Desktop/stage/TensorFlow-Tutorials/inception_uneImage_train.pkl")
    	
        file_path_cache_train = os.path.join(path,"inception_uneImage_train"+str(c)+".pkl")
        print("Processing Inception transfer-values for training-images ...")
       
        # If transfer-values have already been calculated then reload them,
        # otherwise calculate them and save them to a cache-file.
        transfer_values_train = transfer_values_cache(cache_path=file_path_cache_train,
    		                                      images=image,
    		                                      model=model)
        
        out.append(transfer_values_train)
    return out

def generationMusique() :
    
    return

import pickle

def mainIdea1Part1(imagesNames, path, listVideosRef, ideaNb=1, extraction=0) :
        #extracts and computes features from references :
        featsRef=[]
        listVideosRef= [path+n for n in os.listdir(path) if n[-4:]=='.mp4']
        if extraction == 1 :
            for video in listVideosRef :
                extractionImages.extractionImagesAndSounds(video, "png", "wav", 5, 10)
            rename(listVideosRef)
        print("ren")
        a=0
        for name in listVideosRef :
            a+=1
            print(name, a)
            featsRef.append(features.featuresImages(name, path))
        np.save(path+"featsRefImages"+".npy",featsRef)
        print("saved")
        #work with the images given in parameters :
        imagFeats = featuresImages(path, imagesNames) #computes the features for all the images
        f= np.load(path+"featsRefImages"+".npy")
        sounds=[]
        featsMeans=[]
        print("loaded")
        if ideaNb==2 :
            while(len(imagFeats)>0) :
                if len(imagFeats >=3) :
                    featsMeans.append((np.array(imagFeats[0])+np.array(imagFeats[1])+np.array(imagFeats[2]))/3)
                    imagFeats=imagFeats[3:]
                elif len(imagFeats) ==2 :
                    featsMeans.append((np.array(imagFeats[0])+np.array(imagFeats[1]))/3)
                    imagFeats=imagFeats[2:]
                elif len(imagFeats)==1 :
                    featsMeans.append(np.array(imagFeats[0]))
                    imagFeats=imagFeats[1:]
        elif ideaNb==1 :
            featsMeans=imagFeats
        print("here")
        for extract in featsMeans :
            neighbours= generation.closest(extract, f)[0]
            sounds.append(neighbours)
        print("end")
        f=open("closests", "wb")
        pickle.dump(sounds, f, protocol=2)
        f.close()
        
        return 

import subprocess
def rename(listVideosRef) :
    directory = "datasets/YourMusicLibrary/"
    if (not (os.path.isdir(directory))) :
        os.makedirs(directory, mode=0o777)
    else :
        shutil.rmtree(directory)
        os.makedirs(directory, mode=0o777)
    compteur=0
    for video in listVideosRef :
        compteur+=1
        for soundName in os.listdir(video[:-4]+"son"):
            src= video[:-4]+"son/"+soundName
            dst=directory+"v"+str(compteur)+soundName[:-4]+".mp3"
            c="ffmpeg -i "+src+" -codec:a libmp3lame -qscale:a 2 "+dst
            subprocess.call(c, shell=True)

        
    return 

def mainIdea1Part2(path, imagesNames) :
    n=0
    liste=[]
    while len(imagesNames)>0 :
        n+=1
        if len(imagesNames)>=3 :
            imagesNb=imagesNames[:3]
            imagesNames=imagesNames[3:]
        elif len(imagesNames) == 2:
            imagesNb=imagesNames[:2]
            imagesNames=imagesNames[2:]
        else :
            imagesNb=imagesNames
            imagesNames=[]
        soundName = path + "sound"+str(n)+".wav"
        
            
        generation.generateVideo(soundName, imagesNb, [], path, 2.5, "yes", str(n) ) # now we have created many videos that lasts 15seconds with 3images and one music
        liste.append(path+"output/videoFinale"+str(n)+".mp4")
    listeBis = []
    for name in liste :
        listeBis.append(mp.VideoFileClip(name))
    video = mp.concatenate_videoclips(listeBis)
    video.write_videofile(path+"output/videoFinale"+"all"+".mp4") 
    return


import argparse

parser = argparse.ArgumentParser()

parser.add_argument("part", default=1)
parser.add_argument('-i','--list', nargs='+', help='<Required> Set flag', required=True)
parser.add_argument("-p","--path")
parser.add_argument("-e", "--extraction", nargs='?', default=1)
parser.add_argument("-nb", "--ideaNb", nargs='?', default = 1)
args = parser.parse_args()

if int(args.part)==1 :
    mainIdea1Part1(args.list, args.path, int(args.ideaNb), int(args.extraction))
elif int(args.part)==2 :
    mainIdea1Part2(args.path, args.list)


