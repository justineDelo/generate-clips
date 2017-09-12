#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 11:31:06 2017

@author: justine
"""
import numpy as np
import extractionImages
from generationV1 import closests
import features
import matplotlib.pyplot as plt
import subprocess
import concatenate
import os
path='/home/media/justine/Maxtor1/TB1A/stage/' # path to the location of the reference videos and the repertories containing the image and sounds extracted from them
width = 0.5 # time in seconds corresponding to half the time of an extract
videosDirectory = "stage"
listVideosRef= [videosDirectory+"/"+n for n in os.listdir(videosDirectory) if n[-4:]=='.mp4']# all the names of the reference videos
musicName = 'video1.mp4'




def featuresImagesWithAutoencoder(videoName, encoder) :
    images = extractionImages.extractionImagesAndSounds(videoName)
    print(np.array(images).shape)
    out=[]
    c=0
    for im in images :
        c+=1
        image=[im]
        x=encoder.predict(image)
        out.append(x)
        
    return 

def featuresWithAutoencoder(videoName, encoder) :
    images = featuresImagesWithAutoencoder(videoName, encoder) # includes the extraction of image and sound
    sounds=features.featuresAudio(videoName)
    couples=[[images[i],[sounds[i]]]for i in range(0, len(images))]
    return couples

def featuresManyVideosWithAutoencoder(listNames, encoder) :
    """
    for a video, it cuts into samples of images and sounds and then for each extract obtained, give the feature vectors for the sound and the image
    it returns :
        [[[[featImagefromVid1Extract1], [featAudioVid1Extract1]],[[featImageVid1Extract2], [featAudioVid1Extract2]]],[[[featImageVid2Extract1],[featAudioVid2Extract2]]]]
    """
    f=[]

    for name in listNames :
        f.append(featuresWithAutoencoder(name, encoder))
    return f


def featuresRefInfileWithAutoencoder(listVideosRef, encoder) :
    featuresRefCouple=featuresManyVideosWithAutoencoder(listVideosRef, encoder)
    np.save("featsRefAutoencoder.npy",featuresRefCouple)
    return


def featsRefReadWithAutoencoder() :
    feats = np.load("featsRefAutoencoder.npy")
    return feats

def generateVideo2(soundName, featImages, decoder) :
    """
        this function generate the video from the music you want knowing which feature_image needs to be associated for each extract of music

    """
    compteur=1
    name="portion1"
    soundName=path+"\\"+soundName[:-4] + "son\\sound1.wav"
    listeVideosNames=[]
    for feat in featImages :
        
        listeVideosNames.append(name+".mp4")
        image = decoder.predict(feat)
        plt.imsave(name+"imageCree.png",image)
        # convert wav into mp3
        c1="ffmpeg -i "+soundName+" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "+soundName[:-4]+".mp3"
        subprocess.call(c1, shell=True)
        #then create a video with the right duration containing only the image
        c2="ffmpeg -loop 1 -i "+name+"imageCree.png"+" -c:v libx264 -t "+str(int(2*width))+" -pix_fmt yuv420p -vf scale=320:240 "+name+"im.mp4"
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

def all(musicName,n=10) :   
    import autoencoder.py
    encoder, decoder = autoencoder.train()
    print("trained")
    featuresRefInfileWithAutoencoder(listVideosRef, encoder)
    print("featRef")
    f=featsRefReadWithAutoencoder() # pour recuperer la matrice cree juste avant
    featImages = generateFeatImages(musicName, f,n)
    print("featureImage generee")
    generateVideo2(musicName, featImages, decoder)
    print("the end")

    return


def combinliste(seq, k):
    """
    example : seq=[1,2,3], k=2 : it returns : [[1,2], [1,3], [2,3]]
    """
    p = []
    i, imax = 0, 2**len(seq)-1
    while i<=imax:
        s = []
        j, jmax = 0, len(seq)-1
        while j<=jmax:
            if (i>>j)&1==1:
                s.append(seq[j])
            j += 1
        if len(s)==k:
            p.append(s)
        i += 1 
    return p

#all the elements from possibilities are used, all the coeffs are 1 or -1
def combLinCoefs1(possibilities, extract, featuresRefCouple) :
    nbPositions = len(possibilities)
    positions = [j for j in range(1, nbPositions+1)]
    positionsPlus=[]
    dicoDesFeatures={}
    dMin=float('inf')
    for i in range(1,len(possibilities)+1) : #i is the number of '+'
        positionsPlus.append(combinliste(positions,i))
    for couple in possibilities :
        indice = "video"+str(couple[0])+"extract"+str(couple[1])
        dicoDesFeatures[indice] = featuresRefCouple[couple[0]][couple[1]][1][0]
    for nbdePlus in positionsPlus :
        for combinaison in nbdePlus :
            valeur = np.zeros(np.array(extract).shape)
            for position in positions :
                indice = "video"+str(possibilities[position-1][0])+"extract"+str(possibilities[position-1][1])
                if position in combinaison :
                    valeur+=dicoDesFeatures[indice]
                else :
                    valeur-=dicoDesFeatures[indice]
            distance =0
            for sec in range(len(valeur)) :
                for caract in range(len(valeur[sec])) :
                    distance += abs(extract[sec][caract]-valeur[sec][caract])
            if (distance <dMin) :
                if (distance==0) :
                    print('d0', combinaison)
                dMin=distance
                best = combinaison      
            
                
    return best, possibilities

def featImageComposed1(featuresRefCouple, possibilities, coefs) :
    dicoDesFeatures={}
    for couple in possibilities :
        indice = "video"+str(couple[0])+"extract"+str(couple[1])
        dicoDesFeatures[indice] = featuresRefCouple[couple[0]][couple[1]][0]
    feature = np.zeros(np.array(dicoDesFeatures[indice]).shape)
    nbPositions = len(possibilities)
    positions = [j for j in range(1, nbPositions+1)]
    for position in positions :
        indice = "video"+str(possibilities[position-1][0])+"extract"+str(possibilities[position-1][1])
        if position in coefs :
            feature+=dicoDesFeatures[indice]
        else :
            feature-=dicoDesFeatures[indice]
    
    return feature


#les deux fonctions précédentes permettent de choisir la combinaison linéaire(avec uniquement des -1 et +1) des n features les plus proches de manière à ce que l'écart avec le feature recherché soit le plus faible possible



def closestDist(extract, dicoDesFeatures) :
    dMin=float('inf')
    plusOuMoins='null'
    bestIndice='null'
    for indice in dicoDesFeatures :
        distance1=0
        distance2=0
        #print("ind", indice)
        for sec in range(len(dicoDesFeatures[indice])) :
            for caract in range(len(dicoDesFeatures[indice][sec])) :
                    distance1 +=(extract[sec][caract]-dicoDesFeatures[indice][sec][caract])
                    distance2 += (extract[sec][caract]+dicoDesFeatures[indice][sec][caract])
        #print(distance1, distance2)
        if (abs(distance1) <abs(dMin) or abs(distance2)<abs(dMin)) :
            if abs(distance1)<abs(distance2) :
                dMin=distance1
                plusOuMoins=1
            else :
                dMin=distance2
                plusOuMoins=2
            bestIndice = indice
                       
    return bestIndice, dMin, plusOuMoins
        
        

def combLinV2(possibilities, extract, featuresRefCouple) :
    dicoDesFeatures={}
    dicoDesCoefs={}
    continuer=1

    for couple in possibilities :
        indice = str(couple[0])+","+str(couple[1])
        dicoDesCoefs[indice]=[]
        dicoDesFeatures[indice] = featuresRefCouple[couple[0]][couple[1]][1][0]

    distanceAZero=np.array(extract).sum()

    while(continuer==1) :
        bestIndice, distanceMin, plusOuMoins = closestDist(extract, dicoDesFeatures)
        print(distanceMin, distanceAZero)
        if abs(distanceMin)>=abs(distanceAZero):
            continuer=0
        else :     
            if plusOuMoins== 1 :
                dicoDesCoefs[bestIndice].append('+')
                extract = extract- dicoDesFeatures[bestIndice]
            elif plusOuMoins == 2 :
                dicoDesCoefs[bestIndice].append('-')
                extract = extract + dicoDesFeatures[bestIndice]
            if distanceMin==0 :
                continuer=0
            distanceAZero = extract.sum()
    return dicoDesCoefs

def featImageComposedV2(featuresRefCouple, dicoDesCoefs) :
    dicoDesFeaturesImages={}
    for indice in dicoDesCoefs :
        ind=indice
        dicoDesFeaturesImages[indice] = featuresRefCouple[int(indice.split(",")[0])][int(indice.split(",")[1])][0]

    feature = np.zeros(np.array(dicoDesFeaturesImages[ind]).shape)
    for indice in dicoDesCoefs :
        for elt in dicoDesCoefs[indice] :
            if elt=='+':
                feature+=dicoDesFeaturesImages[indice]
            elif elt =='-':
                feature-=dicoDesFeaturesImages[indice]
    return feature

def generateFeatImages(musicName, featuresRefCouple, n=10) :
    extractionImages.JustSoundsExtracts(musicName)
    featAudio = features.featuresAudio(musicName)
    featImages=[]
    for extract in featAudio :
        possibilities=closests(extract, featuresRefCouple,n)[0]
        coefs = combLinV2(possibilities, extract, featuresRefCouple)
        featImages.append(featImageComposedV2(featuresRefCouple, coefs))
    return featImages
