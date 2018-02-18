'''
To create vectors and perform operations 
'''
from math import log

def create_tf_vector(incidence_mat, document):
	'''
	Creating a term freq vector using incidence matrix
	Document here should be list of words
	'''
	tf_vector = list()
	for term in incidence_mat.keys():
		T = len(document)
		tf = document.count(term)
		tf_vector.append(tf / T)

	return tf_vector

def create_idf_vector(incidence_mat, N):
	'''
	Creating an inverse doc freq vector using incidence matrix
	N - Total documents in the system
	'''
	idf_vector = list()
	for term, doc_stats in incidence_mat.items():
		doc_freq = len(doc_stats)	# No of docs that contain term
		idf_vector.append(log(N / (1 + doc_freq)))

	return idf_vector

def convert_to_unit(vector):
	'''
	Converts normal vector to unit vector
	'''
	unit_vector = list()
	vector_mag = (sum([x ** 2 for x in vector])) ** 0.5
	for dim in vector:
		unit_vector.append(dim / vector_mag)

	return unit_vector

def unit_cosine(v1, v2):
	'''
	Calculates cosine between two unit vectors
	'''
	cos = 0
	for x,y in zip(v1, v2):
		cos += (x*y)

	return cos