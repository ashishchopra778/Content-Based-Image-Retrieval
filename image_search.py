import pickle
from sqlite3 import dbapi2 as sqlite
from numpy import *
import numpy as np 
import math
import imlist
from pylab import *
from PIL import Image 

images_path="/home/ashish/dip/chap7/images_test/"
images=imlist.get_imlist(images_path) #Get the list of images
nbr_images=len(images)


class Indexer(object):
	def __init__(self,db,voc):
		self.con = sqlite.connect(db)
		self.voc = voc
	
	def __del__(self):
		self.con.close()

	def db_commit(self):
		self.con.commit()

	def create_tables(self):
		self.con.execute('create table imlist(filename)')
		self.con.execute('create table imwords(imid,wordid,vocname)')
		self.con.execute('create table imhistograms(imid,histogram,vocname)')
		self.con.execute('create index im_idx on imlist(filename)')
		self.con.execute('create index wordid_idx on imwords(wordid)')
		self.con.execute('create index imid_idx on imwords(imid)')
		self.con.execute('create index imidhist_idx on imhistograms(imid)')
		self.db_commit()


	def is_indexed(self,imname):
		im = self.con.execute("select rowid from imlist where filename='%s'" % imname).fetchone()
		return im != None

	def get_id(self,imname):
		cur = self.con.execute("select rowid from imlist where filename='%s'" % imname)
		res=cur.fetchone()
		if res==None:
			cur = self.con.execute("insert into imlist(filename) values ('%s')" % imname)
			return cur.lastrowid
		else:
			return res[0]

	def add_to_index(self,imname,descr):
		if self.is_indexed(imname): return
		print 'indexing', imname
		# get the imid
		imid = self.get_id(imname)
		# get the words
		imwords = self.voc.project(descr)
		nbr_words = imwords.shape[0]
		# link each word to image
		for i in range(nbr_words):
			word = imwords[i]
		# wordid is the word number itself
		self.con.execute("insert into imwords(imid,wordid,vocname)values (?,?,?)", (imid,word,self.voc.name))
		# store word histogram for image
		# use pickle to encode NumPy arrays as strings
		self.con.execute("insert into imhistograms(imid,histogram,vocname)values (?,?,?)", (imid,pickle.dumps(imwords),self.voc.name))


class Searcher(object):
	def __init__(self,db):
		self.con=sqlite.connect(db)
		#self.voc=voc

	def __del__(self):
		self.con.close()

	def candidates_from_word(self,imword):
		im_ids = self.con.execute("select distinct imid from imwords where wordid=%d" % imword).fetchall()
		return [i[0] for i in im_ids]

	def candidates_from_histogram(self,imwords):
		words = imwords.nonzero()[0]
		# find candidates
		candidates = []
		for word in words:
			c = self.candidates_from_word(word)
			candidates+=c
		# take all unique words and reverse sort on occurrence
		tmp = [(w,candidates.count(w)) for w in set(candidates)]
		tmp.sort(cmp=lambda x,y:cmp(x[1],y[1]))
		tmp.reverse()
		# return sorted list, best matches first
		return [w[0] for w in tmp]

	def get_imhistogram(self,imname):
		im_id = self.con.execute("select rowid from imlist where filename='%s'" % imname).fetchone()
		s = self.con.execute("select histogram from imhistograms where rowid='%d'" % im_id).fetchone()
		# use pickle to decode NumPy arrays from string
		return pickle.loads(str(s[0]))

	def get_filename(self,imid):
		s = self.con.execute("select filename from imlist where rowid='%d'" % imid).fetchone()
		return s[0]

	def query(self,imname):
		h = self.get_imhistogram(imname)
		candidates = self.candidates_from_histogram(h)
		matchscores = []
		for imid in candidates:
			cand_name = self.con.execute("select filename from imlist where rowid=%d" % imid).fetchone()
			cand_h = self.get_imhistogram(cand_name)
			dist= sum( (h-cand_h)**2 )
			cand_dist = (dist**0.5) #use L2 distance
			matchscores.append( (cand_dist,imid) )
		# return a sorted list of distances and database ids
		matchscores.sort()
		return matchscores

def compute_ukbench_score(src,imlist):
	nbr_images = len(imlist)
	pos = zeros((nbr_images,4))
	# get first four results for each image
	for i in range(nbr_images):
		pos[i] = [w[1]-1 for w in src.query(imlist[i])[:4]]
	# compute score and return average
	score = array([ (pos[i]//4)==(i//4) for i in range(nbr_images)])*1.0
	return sum(score) / (nbr_images)


def plot_results(src,res):
	figure()
	nbr_results = len(res)
	for i in range(nbr_results):
		imname = src.get_filename(res[i])
		subplot(1,nbr_results,i+1)
		imshow(array(Image.open(images_path+imname)))
	axis('off')
	show()

#src=Searcher('test.db')
#nbr_results = 4
#res = [w[1] for w in src.query(images[23])[:nbr_results]]
#plot_results(src,res)


#print(compute_ukbench_score(src,images))