import pickle
import vocabulary
import imlist
import compute_feature
import os

images=imlist.get_imlist("/home/ashish/dip/chap7/images_test/")
features_path="/home/ashish/dip/chap7/features_test/"
nbr_images=len(images)

featureslist=[]
for img in images:
	img_txt=os.path.splitext(img)[0]
	des_file=features_path+img_txt+"des"+".txt"
	featureslist.append(des_file)

print(featureslist)

voc = vocabulary.Vocabulary('ukbenchtest')
voc.train(featureslist,100,10)

with open('vocabulary.pkl', 'wb') as f:
	pickle.dump(voc,f)
print 'vocabulary is:', voc.name, voc.nbr_words
