from numpy import *

def read_features_from_file(filename):
	f = loadtxt(filename,dtype="string")
	return f[:,:] # feature locations, descriptors