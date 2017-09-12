This is a program to generate images to transform a given music into a videoclip.

The code is for python3.6



You need to have the following libraries :
	- subprocess
	- numpy
	- os
	- copy
	- matplotlib
	- resizeimage
	- PIL
	- shutil
	- moviepy
	- mutagen
	- wave
	- contextlib
	- opencv (cv2)
	- tensorflow
	- random
	

You also need to install :
	- xmorph (morph)
	- ffmpeg

You also need the vggish_model.ckpt file so place yourself in the cloned directory and run this in a terminal :
	curl -O https://storage.googleapis.com/audioset/vggish_model.ckpt


To launch the program :

with a terminal, place yourself in the directory containing the file generationV1.py and write :

python generationV1.py musicNamePath path [extractionRef] [computeMatrix] [slidesOrVideos] [width]

There are different parameters :

	- musicNamePath : is the path to the music file on which you want to add images. example : /home/name/repertory/music.wav. The music file has to be in one of the following formats : mp3, wav or mp4

	- path : path to the location of the reference videos and the repertories containing the image and sounds extracted from them. example : /home/name/referencesRepertory/. NB : it's important to write the last '/'

	- extractionRef : facultative, has to be an integer default_value=0. If 0 : the program considers that the extraction of reference images and sounds had already been done. If another value the extraction will be done again. It is a long process so it is not necessary to do it if it has been done before.

	- computeMatrix, facultative, has to be an integer, default value 0. If 0 (and extractionRef = 0 too), then the programm will consider that the features for all the extracted sounds and images from reference videos had already been calculated and won't compute them again. As for extractionRef, this process takes a long time and is not necessary to do several times. the features are saved in a file named featsRef.npy. If you delete this file, it will be necessary to compute the features again. If another value, the features will be calculated again.

	- slidesOrVideos, facultative, has to be one of the following values : 'v', 's1', 'sm'. Default value : 'sm'. 'v' will launch the program that returns a video composed of a concatenation of 1second video extracts from the reference videos. Each one is chosen because the audio associated with it is the closest to the audio from the music file at this moment. 's1' will do the same but with a concatenation of images. 'sm' too but the images will be a mix between the two images corresponding to the two closest audio features.

	- width : facultative, default value 0.5, is half the time for an extract (in seconds). Be careful, if you change this value it is necessary to extract again sounds and images from reference videos and to compute again the reference features (so put extractionRef = 1 and computeMatrix = 1) so that the extracts will all have the same length


