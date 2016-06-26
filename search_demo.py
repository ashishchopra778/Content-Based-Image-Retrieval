import cherrypy
import os
import pickle
import urllib
import imlist
import image_search

class SearchDemo(object):
	def __init__(self):
		self.images=imlist.get_imlist("/home/ashish/dip/chap7/images_test")
		self.nbr_images=len(self.images)
		self.ndx=range(self.nbr_images)
		with open('vocabulary.pkl','rb') as f:
			self.voc=pickle.load(f)

		self.maxres=4

	def index(self):
		self.src=image_search.Searcher('test.db')
		html="""
				<html>
				<head> <title> Content Based Image Retrievel </title> </head>
				<body>
				<h1>Enter the image to be searched for!</h1>
				<form method="get" action="generate">
				<input type="text" name="image_name"/>
				<button type="submit">Find Images</button>
				</form>
				</body>
				</html>
				"""
		return html

	def generate(self,image_name):
		self.src=image_search.Searcher('test.db')
		res=self.src.query(image_name)[:self.maxres]
		html2="<h2>Your query image is <h2> <img src='"+image_name+"'width='300'/> </br> <h2>Best found results are</h2>"
		for dest,ndx in res:
			imname=self.src.get_filename(ndx)
			#print(imname)
			html2+="<img src='"+imname+"' width='300'/>"
		'''footer="""
			</body>
			</html""" 
		html+=footer'''
		return html2
		

	index.exposed=True
	generate.exposed=True

cherrypy.quickstart(SearchDemo(),'/',config=os.path.join(os.path.dirname(__file__),'tutorial1.conf'))

