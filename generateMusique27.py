#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 13:40:33 2017

@author: justine
"""

import pickle
import generate
import subprocess

def retrieveNumbers() :
    f=open("closests", "rb")
    closestsNb=pickle.load(f)
    f.close()
        
    return closestsNb

def createSounds(path, ideaNb=1) :
    closestsNb=retrieveNumbers()
    compteur=0
    while len(closestsNb)>0 :
        compteur+=1
        output_filename = path+"sound"+str(compteur)+".wav"
        print(output_filename)
        if ideaNb == 1 :
            if len(closestsNb)>=3 :
    #            if ideaNb== 3 :
    #                
    #                command= "ffmpeg -i concat:"+indice(closestsNb[0])[1]+"|"+indice(closestsNb[1])[1]+"|"+indice(closestsNb[2])[1]+" -acodec copy melange.mp3"
    #                subprocess.call(command, shell=True)
    #                generate.main(output_filename,1, )
                generate.main(output_filename, 3, indice(closestsNb[0])[0], indice(closestsNb[1])[0], indice(closestsNb[2])[0])
                closestsNb=closestsNb[3:]
            elif len(closestsNb)==2 :
                generate.main(output_filename, 2, indice(closestsNb[0])[0], indice(closestsNb[1])[0])
                closestsNb=closestsNb[2:]
            elif len(closestsNb)==1 :
                generate.main(output_filename, 1, indice(closestsNb[0])[0])
                closestsNb=closestsNb[1:]
        elif ideaNb ==2 :
            generate.main(output_filename, 1, indice(closestsNb[0])[0])
            closestsNb=closestsNb[1:]
    
    return
    


def indice(couple) :
    
    videoNb=couple[0]
    extractNb=couple[1]
    soundName="v"+str(videoNb)+"sound"+str(extractNb)+".wav"
    f=open("filesNames", "rb")
    filesNames=pickle.load(f)
    f.close()
    directory = filesNames[0]
    filesNames=filesNames[1:]
    index=filesNames.index(directory+soundName)
    
    return index, directory+soundName

createSounds("/media/justine/Maxtor1/TB1A/stage/")