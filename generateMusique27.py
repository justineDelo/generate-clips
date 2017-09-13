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
    print (closestsNb[1])
    while len(closestsNb)>0 :
        compteur+=1
        output_filename = path+"sound"+str(compteur)+".wav"
        print(output_filename)
        if ideaNb == 1 :
            if len(closestsNb)>=3 :
                generate.main(output_filename, 3, indice(closestsNb[0])[0], indice(closestsNb[1])[0], indice(closestsNb[2])[0])
                closestsNb=closestsNb[3:]
            elif len(closestsNb)==2 :
                print("ici")
                generate.main(output_filename, 2, indice(closestsNb[0])[0], indice(closestsNb[1])[0])
                print("done")
                closestsNb=closestsNb[2:]
                print("end")
            elif len(closestsNb)==1 :
                generate.main(output_filename, 1, indice(closestsNb[0])[0])
                closestsNb=closestsNb[1:]
        elif ideaNb ==2 :
            generate.main(output_filename, 1, indice(closestsNb[0])[0])
            closestsNb=closestsNb[1:]
    
    return
    


def indice(couple) :
    print(couple)
    videoNb=couple[0]+1
    extractNb=couple[1]+1
    soundName="v"+str(videoNb)+"sound"+str(extractNb)+".wav"
    f=open("filesNames", "rb")
    filesNames=pickle.load(f)
    f.close()
    directory = filesNames[-1]
    print("dir", directory)
    filesNames=filesNames[:-1]
    print(filesNames[0])
    index=filesNames.index(directory+soundName)
    
    return index, directory+soundName

createSounds("/media/justine/Maxtor1/TB1A/stage/")