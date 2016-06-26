import image_search
import pickle
import imlist
import numpy as np 
import os
from numpy import *

def read_features_from_file(filename):
	f = loadtxt(filename,dtype="string")
	return f[:,:] # feature locations, descriptors

images=imlist.get_imlist("/home/ashish/dip/chap7/images_test/")
features_path="/home/ashish/dip/chap7/features_test/"
nbr_images=len(images)

featureslist=[]
for img in images:
	img_txt=os.path.splitext(img)[0]
	des_file=features_path+img_txt+"des"+".txt"
	featureslist.append(des_file)


with open('vocabulary.pkl', 'rb') as f:
	voc = pickle.load(f)

indx = image_search.Indexer('test.db',voc)
#indx.create_tables()

for i in range(nbr_images):
	descr = (read_features_from_file(featureslist[i])).astype(np.float)
	indx.add_to_index(images[i],descr)
# commit to database
indx.db_commit()