#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 13:40:33 2017

@author: justine
"""

import pickle
import generate


def retrieveNumbers() :
    """
    retrieves the couples [videoNb, extractNb] corresponding to each sound chosen to create the new sounds
    """
    f=open("closests", "rb")
    closestsNb=pickle.load(f)
    f.close()
        
    return closestsNb

def createSounds(path, ideaNb=1) :
    """
    this function is the link between what was done in python3.6 (extraction, sounds chosen etc) and the gruv program to generate a new sound
    """
    closestsNb=retrieveNumbers()
    compteur=0
    while len(closestsNb)>0 :
        compteur+=1
        output_filename = path+"sound"+str(compteur)+".wav"
        if ideaNb == 1 :
            if len(closestsNb)>=3 :
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
    """
    this function is used to find the right sound in the list created by train.py (gruv) according to the videoNb and the extractNb retrieved by closest
    """
    videoNb=couple[0]+1
    extractNb=couple[1]+1
    soundName="v"+str(videoNb)+"sound"+str(extractNb)+".wav"
    f=open("filesNames", "rb")
    filesNames=pickle.load(f)
    f.close()
    directory = filesNames[-1]
    filesNames=filesNames[:-1]
    index=filesNames.index(directory+soundName)
    
    return index, directory+soundName

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path")
parser.add_argument("nb")
args = parser.parse_args()

createSounds(args.path, int(args.nb))