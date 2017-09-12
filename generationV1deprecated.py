# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 11:09:12 2017

@author: Utilisateur
"""

import features
import subprocess
import numpy as np
import concatenate
import extractionImages
import os
import shutil
#import json
import matplotlib.pyplot as plt
from resizeimage import resizeimage
from PIL import Image
import moviepy.editor as mp 
import moviepy.video.fx.all as vfx
import random

#parameters
"""
#pathMixImages='/media/justine/Maxtor1/TB1A/stage/Mix/' #path where the composed images will be saved
#path='/media/justine/Maxtor1/TB1A/stage/' # path to the location of the reference videos and the repertories containing the image and sounds extracted from them
pathMixImages='/home/justine/Documents/TB1A/stage/Mix/' 
path='/home/justine/Documents/TB1A/stage/' 

width = 0.5 
listVideosRef= [path+n for n in os.listdir(path) if n[-4:]=='.mp4']
"""


def featuresRefInfile(listVideosRef, path, sOrV) :
    """
    this function retrieves all the features for all the extracts of all the videos and save it in order to not have to do this step that can take a while each time you want to generate a new clip
    """
    featuresRefCouple=features.featuresManyVideos(listVideosRef, path, sOrV)
    np.save(path+"featsRef"+sOrV+".npy",featuresRefCouple)
#    with open(path+'dico.txt', 'w') as file :
#        json.dump(dicoNomsIndices, file)
    return
    


def featsRefRead(path, sOrV) :
    """
    just to retrieve the matrix with all the features for reference videos
    """
    feats = np.load(path+"featsRef"+sOrV+".npy")
#    with open(path+'dico.txt', 'r') as file :
#        dicoNomsIndices  = json.load(file)
    return feats




###################### the functions below are used to generate a videoClip from a music where the images are chosen from reference images ############################

def AudioFeatAndChooseImages(musicName, featuresRefCouple, formatOutputSound, width, freq, sOrV ='s') :
    """
    do several things :
        - cut the music into extract of 2*width seconds
        - then it gives the features for each extract
        - returns a list of couple : [(videoNb, extractNb), (videoNb, extractNb)...]. Each couple corresponds to the image that was chosen to appear during the sound extract corresponding to its index in the list
    """
    extractionImages.JustSoundsExtracts(musicName, formatOutputSound, width, freq)
    featAudio = features.featuresAudio(musicName)
    imageOut = []
    for extract in featAudio :
        imageOut.append(closest(extract, featuresRefCouple, sOrV)[0])
    return imageOut



def closest(extract, featuresRefCouple, sOrV='s', exclus=[]):
    """
    this function is used to compare the audio feature of an extract of your music to every reference extracts
    then, it computes the difference between the features and decides which reference extract is the closest to the extract of the music
    it returns the number of the reference video and the extract of this video that is the closest one so that we can use the reference image initially associated with this extract to illustrate our music extract
    """
    distance = 0
    dMin = float('inf')
    best = [0,0] # [videoNb, extractNb]
    
    for videoNb in range(len(featuresRefCouple)) :
        for extractNb in range(len(featuresRefCouple[videoNb])) :
            if [videoNb,extractNb] not in exclus :
                distance= 0
                if sOrV=='s' :
                    audioFeat = featuresRefCouple[videoNb][extractNb][1] #1*1(duree de l'audio en secondes)*128
                elif sOrV=='v' :
                    audioFeat= featuresRefCouple[videoNb][extractNb]
                for sec in range(len(audioFeat[0])) :
                    for caract in range(len(audioFeat[0][sec])) :
                        distance += abs(extract[sec][caract]-audioFeat[0][sec][caract])
                if (distance <dMin) :
                    if (distance==0) :
                        print('d0', videoNb, extractNb)
                    dMin=distance
                    best = [videoNb, extractNb]      
            
    return best, dMin

def generateVideo(soundName, imagesNb, listVideosRef, path, width ) :
    """
    this function generate the video from the music you want knowing which image needs to be associated for each extract of music
    """
    compteur=1
    name="portion1"
    soundName=path+"\\"+soundName[:-4] + "son\\sound1.wav"
    listeVideosNames=[]
    for im in imagesNb :
        listeVideosNames.append(name+".mp4")
        VidNb=im[0]
        extractNb = im[1]
        imageName = path + "\\"+listVideosRef[VidNb][:-4] + "\\im"+str(extractNb+1)+listVideosRef[VidNb]+".png"
        # convert wav into mp3
        c1="ffmpeg -i "+soundName+" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "+soundName[:-4]+".mp3"
        subprocess.call(c1, shell=True)
        #then create a video with the right duration containing only the image
        c2="ffmpeg -loop 1 -i "+imageName+" -c:v libx264 -t "+str(int(2*width))+" -pix_fmt yuv420p -vf scale=320:240 "+name+"im.mp4"
        subprocess.call(c2, shell=True)
        #add the sound
        c3="ffmpeg -i "+name+"im.mp4 -i "+soundName[:-4]+".mp3"+" -codec copy -shortest "+name+".mp4"
        subprocess.call(c3, shell=True)
        name="portion"+str(compteur+1)
        print(name)
        compteur+=1
        if compteur <=10:
            soundName = soundName[:-5]+str(compteur)+".wav"
        elif compteur <=100 :
            soundName = soundName[:-6]+str(compteur)+".wav"
        elif compteur <= 1000 :
            soundName = soundName[:-7]+str(compteur)+".wav"
        elif compteur <= 10000 :
            soundName = soundName[:-8]+str(compteur)+".wav"
        print(soundName)
    concatenate.concatenate2(listeVideosNames[1:])
            
    return

#tout function takes only the closestImage 
def tout(path, listVideosRef, formatOutputSound, width, freq) :
    """
    this function supposes that the reference extracts and images have already been extracted from the reference videos
    but do all the necessary things after this step : from computing the audio and image features of the reference extracts to the creation of a video for a new music
    """
    featuresRefInfile(listVideosRef, path, 's') # pour creer et enregistrer la matrice des features audio et images de toutes les videos de reference
    f=featsRefRead(path, 's') # pour recuperer la matrice cree juste avant
    imagesNb=AudioFeatAndChooseImages("fdelavega.mp3", f, formatOutputSound, width, freq, 's') # pour savoir pour une musique donnee quelle image on doit recuperer pour chaque portion de 4secondes de son, ici l'image est à chaque fois une des videos de reference (cf fonction closest)
    generateVideo("fdelavega.mp3", imagesNb, listVideosRef, path, width) # cree la video correspondante
    return


    
################################# the functions below are used to generate a videoclip from music where the images are made from a composition of two reference images ############################

def closests(extract, frc,n=10) :
    """
    returns the nth closests extracts comparing their audio features
    """
    exclus=[]
    distances=[]

    possibilities=[]
    neighbour, d = closest(extract, frc)
    
    possibilities.append(neighbour)
    distances.append(d)
    exclus.append(neighbour)
    for i in range(n-1) :
        neighbour, d = closest(extract, frc, exclus)
        possibilities.append(neighbour)
        exclus.append(neighbour)
        distances.append(d)
        print(neighbour)
    return possibilities, distances
    

def composition(musicName, featuresRefCouple, pathMixImages, listVideosRef, formatOutputSound, width, freq, n=2) :
    """
    this function does several things :
        - cuts the music into small extracts
        - computes the audio features for each extract
        - selects the two closest reference audio extract for each new extract
        - for each extract, generates an image composed of the two images associated with the two selected reference extracts 
    """
    extractionImages.JustSoundsExtracts(musicName, formatOutputSound, width, freq)
    
    print(musicName)
    featAudio = features.featuresAudio(musicName)
    compteur=0
    for extract in featAudio :
        possibilities, distances=closests(extract, featuresRefCouple,n)
        d1=distances[0]
        d2=distances[1]
        x=d1/d2
        p2=1/(x+1)
        #p1=1-p2
        compteur+=1
        
        outname = pathMixImages+'im'+str(compteur)+'.tga'
        print(outname)
        image1 = listVideosRef[possibilities[0][0]][:-4]+'/im'+str(possibilities[0][1]+1)+'.png'
        #image1 = path+ 'video__'+str(possibilities[0][0])+'_/im'+str(possibilities[0][1])+'.png'
        image2 = listVideosRef[possibilities[1][0]][:-4]+'/im'+str(possibilities[1][1]+1)+'.png'
        #image2 = path+ 'video__'+str(possibilities[1][0])+'_/im'+str(possibilities[1][1])+'.png'
        print("go xmorph")
        xmorph(image1, image2, p2, outname)
        print("end xmorph")
        
    return
        
def generateVideoMP4extracts(musicName, formatOutputSound, width, freq, featuresRefCouple, listVideosRef, path) :
    extractsChosen = AudioFeatAndChooseImages(musicName, featuresRefCouple, formatOutputSound, width, freq, 'v')
    liste=[]
    audio = mp.AudioFileClip(musicName)
    for vid in extractsChosen:
        name = listVideosRef[vid[0]][:-4]+"vid/"+"vid"+str(vid[1])+".mp4"
        liste.append(name)
    video=mp.concatenate_videoclips(liste).set_audio(audio)
    video.write_videofile(path+"output/videoFinale.mp4")
    return

def xmorph(image1, image2, p2, outname) :
    """
    this function generates a new image from two given images and a percentage corresponding to how much it has to look like the second one
    """
    #reshape : both images should have the same dimensions
    im1 = np.array(plt.imread(image1))
    im2=np.array(plt.imread(image2))
    w = min(im1.shape[0], im2.shape[0])
    h = min(im1.shape[1], im2.shape[1])
    
    with open(image1, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [w, h], validate=False)
            if os.path.isfile(image1[:-4]+"resized"+image1[-4:]) :
                os.remove(image1[:-4]+"resized"+image1[-4:])
            cover.save(image1[:-4]+"resized"+image1[-4:], image.format)
    with open(image2, 'r+b') as f :
        with Image.open(f) as image :
            cover = resizeimage.resize_cover(image, [w, h], validate=False)
            if os.path.isfile(image2[:-4]+"resized"+image2[-4:]) :
                os.remove(image2[:-4]+"resized"+image2[-4:])
            cover.save(image2[:-4]+"resized"+image2[-4:], image.format)
    c='convert '+image1[:-4]+"resized"+image1[-4:]+' '+image1[:-3]+'tga'
    subprocess.call(c, shell=True)
    c='convert '+image2[:-4]+"resized"+image2[-4:]+' '+image2[:-3]+'tga'
    subprocess.call(c, shell=True)
    c='morph -start '+image1[:-3]+'tga'+' -finish '+image2[:-3]+'tga'+' -out '+outname+' -mt 1 -dt '+ str(p2)

    subprocess.call(c, shell=True)
    return



def generateVideoWithComposedImages(soundName, listVideosRef, pathMixImages, width, path ) :
    """
        this function generates the video from the music you want knowing which composed_image needs to be associated for each extract of music
    """
    compteur=1
    name=path + "output/portion1"
    soundName=soundName[:-4] + "son/sound1.wav"
    listeVideosNames=[]
    imagesNames = [pathMixImages+n for n in os.listdir(pathMixImages) if n[-4:]=='.tga']
    for imageName in imagesNames :
        listeVideosNames.append(name+".mp4")
        # convert wav into mp3
        c1="ffmpeg -i "+soundName+" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "+soundName[:-4]+".mp3"
        subprocess.call(c1, shell=True)
        #then create a video with the right duration containing only the image
        c2="ffmpeg -loop 1 -i "+imageName+" -c:v libx264 -t "+str(int(2*width)-0.001)+" -pix_fmt yuv420p -vf scale=320:240 "+name+"im.mp4"
        subprocess.call(c2, shell=True)
        #add the sound
        c3="ffmpeg -i "+name+"im.mp4 -i "+soundName[:-4]+".mp3"+" -codec copy -shortest "+name+".mp4"
        subprocess.call(c3, shell=True)

        name=path+"output/"+"portion"+str(compteur+1)
        print(name)     
        compteur+=1
        if compteur <=10:
            soundName = soundName[:-5]+str(compteur)+".wav"
        elif compteur <=100 :
            soundName = soundName[:-6]+str(compteur)+".wav"
        elif compteur <= 1000 :
            soundName = soundName[:-7]+str(compteur)+".wav"
        elif compteur <= 10000 :
            soundName = soundName[:-8]+str(compteur)+".wav"
        print(soundName)
    concatenate.concatenate2(listeVideosNames[1:], path+"output/videoFinale.mp4")
    return

def generateVideoWithComposedImagesV2(soundName, pathMixImages, width, path) :
    """
    this function generates the video from the music you want knowing which composed_image needs to be associated for each extract of music with another method, it improves the result because otherwise it was easy to hear the moment when the image was changing 
    """
    audio = mp.AudioFileClip(soundName)
    compteur=1
    name=path + "output/portion1"
    imagesNames = [pathMixImages+n for n in os.listdir(pathMixImages) if n[-4:]=='.tga']
    for imageName in imagesNames :
        c2="ffmpeg -loop 1 -i "+imageName+" -c:v libx264 -t "+str(int(2*width)-0.001)+" -pix_fmt yuv420p -vf scale=320:240 "+name+".mp4"
        subprocess.call(c2, shell=True)
        compteur+=1
        name=path+"output/portion"+str(compteur)
    cle = lambda x: int(x[7:-4])
    listImagesNames=os.listdir(path+"output/")
    listImagesNames.sort(key=cle)
    liste = []
    for name in listImagesNames :
        liste.append(mp.VideoFileClip(path+"output/"+name))
    #liste = add_effects(liste)
    video=mp.concatenate_videoclips(liste).set_audio(audio)
    video.write_videofile(path+"output/videoFinale.mp4")
    return

def add_effects(liste) :
    duration=0.12
    out=[]
    for clip in liste :
        nb=random.randint(0,13)
        print(nb)
        nb=5
        if (nb ==1 or nb==6 or nb==7 or nb==8 or nb==12):
            color=random.random()
            out.append (clip.fx(vfx.fadein,duration,color))
        elif (nb == 2 or nb==9 or nb==10 or nb==13):
            color = random.random()
            out.append(clip.fx(vfx.fadeout,duration, color))
            
        elif (nb == 3) :
            out.append(clip.fx(vfx.mirror_x))
        elif (nb == 4 or nb==11) :
            out.append(clip.fx(vfx.mirror_y))
#        elif( nb==5 or nb==14 or nb==15):
#            #value=random.randint(0,30)
#            value=20
#            out.append(clip.fx(vfx.rotate,value))
        else :
            out.append(clip)
    return out
        

def toutAvecMelangeDImages(musicName, path, extractionRef, computeMatrix, sOrV, width, formatOutput, formatOutputSound) :
    listVideosRef= [path+n for n in os.listdir(path) if n[-4:]=='.mp4'] # all the names of the reference videos
    if sOrV == 's' :
        pathMixImages = path+'Mix/' #path where the composed images will be saved
#        if (not (os.path.isdir(pathMixImages))) :
#            os.makedirs(pathMixImages, mode=0o777)
#        else :
#            shutil.rmtree(pathMixImages)
#            os.makedirs(pathMixImages, mode=0o777)
#        
#    if (not (os.path.isdir(path+'output/'))) :
#        os.makedirs(path+'output/', mode=0o777)
#    else :
#        if (not(os.path.isdir(path+'output_'+"renamed"))) :
#            os.renames(path+'output', path+"output_"+"renamed/")
#        else :
#            shutil.rmtree(path+"output_"+"renamed")
#            os.renames(path+"output/", path+"output_"+"renamed/")
#        os.makedirs(path+"output/", mode=0o777)
    freq = int(2*width) #to retrieve images from the video with freq seconds between each
    
    if extractionRef == 1 :
        for video in listVideosRef[12:] :
            if sOrV=='s' :
                extractionImages.extractionImagesAndSounds(video, formatOutput, formatOutputSound, width, freq) #extraction for the reference videos
            elif sOrV =='v' :
                extractionImages.extractionVideosExtractsAndSounds(video, width, freq, formatOutputSound)
        featuresRefInfile(listVideosRef, path, sOrV) # pour creer et enregistrer la matrice des features audio et images de toutes les videos de reference
    elif computeMatrix == 1 :
        featuresRefInfile(listVideosRef, path, sOrV)
    f=featsRefRead(path, sOrV) # pour recuperer la matrice creee juste avant
    print(path, len(f))
    if sOrV=='s' :
        composition(musicName, f, pathMixImages, listVideosRef, formatOutputSound, width, freq) # to cut the music, extract features and generate the composed images 
        generateVideoWithComposedImagesV2(musicName, pathMixImages, width, path) # cree la video correspondante
    elif sOrV == 'v' :
        generateVideoMP4extracts(musicName, formatOutputSound, width, freq, f, listVideosRef, path)

    return



import argparse


parser = argparse.ArgumentParser()
parser.add_argument("musicName")
parser.add_argument("path") # path to the location of the reference videos and the repertories containing the image and sounds extracted from them
parser.add_argument("extractionRef", nargs='?', default="0")
parser.add_argument("computeMatrix", nargs='?', default="0")
parser.add_argument("slidesOrVideos", nargs='?', default='s')
parser.add_argument("width", nargs='?', default="0.5") # time before and after the instant of the image saved, time in seconds corresponding to half the time of an extract
parser.add_argument("formatOutput", nargs='?', default='png')
parser.add_argument("formatOutputSound", nargs='?', default = "wav")

args = parser.parse_args()


toutAvecMelangeDImages(args.musicName, args.path,  int(args.extractionRef), int(args.computeMatrix),args.slidesOrVideos,float(args.width), args.formatOutput, args.formatOutputSound)

