
import numpy as np

import os


# Functions and classes for loading and using the Inception model.
import inception

import test_audioset
import matplotlib.pyplot as plt


def featuresImages(videoName, path) :
    """
    this function takes a video in parameter and then open the repertory containing the images already extracted from this video
    It computes a feature vector using inception for each of these images and returns an array with all the features
    """
    #extractionImages.extractionImagesAndSounds(videoName)
    images=[]
    imagesPaths=[n for n in os.listdir(videoName[:-4])]
    cle = lambda x : int(x[2:-4])
    imagesPaths.sort(key=cle)
    for ima in imagesPaths :
        images.append(plt.imread(videoName[:-4]+'/'+ima))

    
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

    
def featuresAudio(videoName) :
    """
    it takes a video in parameter and opens the repertory containing the 1second sound extracts for this video
    for each, it uses audioset to compute a feature vector 
    it returns an array with all the features
    """
    path2=videoName[:-4]+"son"
    outsound=[]
    cle = lambda x: int(x[5:-4])
    listNames=os.listdir(path2)
    listNames.sort(key=cle)
    for element in listNames:
       
        if( not os.path.isdir(element)):
            if (element[-3:]=="wav"):
                outsound.append(test_audioset.main(path2+"/"+element))
            
    return np.array(outsound)



def features(videoName, path) :
    """
    for one video it computes the sound features and returns them for each extract
    """
    
    sounds=featuresAudio(videoName)
#    if sOrV == 's' :
#        images = featuresImages(videoName, path) 
#        couples=[[images[i],[sounds[i]]]for i in range(0, len(images))]
#    else :
#        couples = sounds
#    return couples
    return sounds


def featuresManyVideos(listNames, path) :
    """
    for a video, it gives the feature vectors for the sounds extracted
    it returns :
        [[[featAudioVid1Extract1],[featAudioVid1Extract2]],[[[featAudioVid2Extract2]]]]
    """
    f=[]
    #indice=0
    #dicoNameIndices={}
    for name in listNames :
        print(name)
        #dicoNameIndices[indice]=name
        f.append(features(name, path))
    return f

