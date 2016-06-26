from scipy.cluster.vq import *
from numpy import *
import numpy as np

features_path="/home/ashish/dip/chap7/features/"


def read_features_from_file(filename):
	f = loadtxt(filename,dtype="string")
	return f[:,:] # feature locations, descriptors

class Vocabulary(object):
	def __init__(self,name):
		self.name=name
		self.voc=[]
		self.idf=[]
		self.trainingdata=[]
		self.nbr_words=0

	def train(self,featurefiles,k=100,subsampling=10):
		nbr_images=len(featurefiles)
		descr=[]
		descr.append(read_features_from_file(featurefiles[0]).astype(np.float))
		print("started reading features")
		descriptors = descr[0]
		for i in arange(1,nbr_images):
			descr.append(read_features_from_file(featurefiles[i]).astype(np.float))
			descriptors = vstack((descriptors,descr[i]))
			print(i)

		self.voc,distortion = kmeans(descriptors[::subsampling,:],k,1)
		self.nbr_words = self.voc.shape[0]

		print("started projecting")
		j=0
		imwords = zeros((nbr_images,self.nbr_words))
		for i in range( nbr_images ):
			imwords[i] = self.project(descr[i])
			j=j+1
			print(j)

		nbr_occurences = sum( (imwords > 0)*1 ,axis=0)
		self.idf = log( (1.0*nbr_images) / (1.0*nbr_occurences+1) )
		self.trainingdata = featurefiles

	def project(self,descriptors):
		imhist=zeros((self.nbr_words))
		words,distance = vq(descriptors,self.voc)
		for w in words:
			imhist[w]+=1
		return imhist

















