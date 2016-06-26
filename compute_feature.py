import imlist
import SIFT
import numpy as np 
import os
from scipy.cluster.vq import *

def compute_feature():
	features_path="/home/ashish/dip/chap7/features_test/"
	images_path="/home/ashish/dip/chap7/images_test/"

	images=imlist.get_imlist(images_path) #Get the list of images
	nbr_images=len(images)

	kplist = []
	deslist=[]

	for img in images: #Create KP and desc files for each image
		img_txt=os.path.splitext(img)[0]

		kp_file=features_path+img_txt+"kp"+".txt"
		des_file=features_path+img_txt+"des"+".txt"
	
		kplist.append(kp_file)
		deslist.append(des_file)
	
		kp,des=SIFT.SIFT(images_path+img)
	
		np.savetxt(kp_file,kp,fmt="%s")
		np.savetxt(des_file,des,fmt="%s")
	
	return deslist