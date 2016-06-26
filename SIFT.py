import cv2
import numpy as np
from PIL import Image

def SIFT(name):
	sift = cv2.SIFT()
	img=np.array(Image.open(name).convert('L'))
	kp,des = sift.detectAndCompute(img,None)
	return kp,des
	
