This is a program to generate music in order to transform given photos into a videoclip.

This code needs python3.6 and python2.7

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
	- pickle

You also need to install ffmpeg

You also need the vggish_model.ckpt file so place yourself in the cloned directory and run this in a terminal :
	curl -O https://storage.googleapis.com/audioset/vggish_model.ckpt

To launch the program :

with a terminal, place yourself in the directory containing the files generateMusic.py, convert_directory.py, generateMusique27.py and train.py.

Then, follow the differents steps :

1) write :

python3.6 generateMusic.py part -i pathImage1 pathImage2 ... pathImagen -p path -e extraction -nb nb

the different parameters are :

	- part : must be 1 here
	- pathImage : for each image you want to give in parameter write the path to this image, example : /home/name/Images/image1.jpeg
	- path : is the directory containing the references videos. It should end with '/'
	- extraction : must be 0 or 1. If it is one the extraction of images and sounds to have 10seconds extracts is done. Not necessary if it has already been done in the past.  If 0, it considers that it has already been done.	
	- nb : is the version you want to use. Must be 1 or 2. There are two versions available :the first one uses 3 music reference to create a sound for 3 photos, the second one uses only one. (see principle for more information)



2) write :

python2.7 convert_directory.py

3) write :

python2.7 train.py

4) write :

python2.7 generateMusique27.py path nb

	the different parameters are :
		- path : is the path to the directory containing the reference videos. It should end with /
		- nb : is the version you want to use. Must be 1 or 2. There are two versions available :the first one uses 3 music reference to create a sound for 3 photos, the second one uses only one. (see principle for more information).

5) write :
	python3.6 generateMusic.py part -i pathImage1 pathImage2 ... pathImagen -p path -nb nb

	the different parameters are :

		- part : must be 2 here
		- pathImage : for each image you want to give in parameter write the path to this image, example : /home/name/Images/image1.jpeg
		- path : is the directory containing the references videos. It should end with '/'
		- nb : is the version you want to use. Must be 1 or 2. There are two versions available :the first one uses 3 music reference to create a sound for 3 photos, the second one uses only one. (see principle for more information)

	Be careful to put the same parameters as for the first step except for the first parameter

6) Your video is now available in the directory : path/output/videoFinaleall.mp4

##########################################################################

Principle :

To generate new sounds I used GRUV : https://github.com/mattpearson/GRUV
This code returns a videoclip with the photos given in parameters : a photo lasts 5 seconds and the music changes every 3 photos(15 seconds)

This code uses many references videos that you need to have in your computer. Then it cuts and saves 10second extracts in each videos and separates sound and images remembering which sound is associated to which image. Then, caracterization vectors are computed for each image.
For the images given in parameter, vectors are computed to.
Then, there are two options :
For the first one, each vector image (for images given in parameters) is compared to all the reference vectors and is associated to the most similar one. So, for each image in parameter we associate a reference vector image that's to say a reference image that's to say a reference sound. To generate the sound associated with three photos, a sum of the three reference sounds chosen is given as a start point to generate the new sound (seed_seq in gruv).
For the second one, the program computes the mean of the three vectors to have a new one. And only this new one is compared with the refernce vectors to associate only one sound with these three images. This ousnd is given as a start point to generate the new sound.

Then a diaporama is created with all yout photos and the sounds created.





