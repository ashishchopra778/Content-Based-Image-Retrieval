import os
def get_imlist(path):
	return [os.path.join(f) for f in os.listdir(path) if f.endswith('.jpg')]

	
