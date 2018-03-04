import copy
from collections import OrderedDict
from .files import read_from_json
from .linguistics import preprocessor
from .vectoropt import create_tf_vector, create_idf_vector, convert_to_unit, unit_cosine_calc

def relevant_K_bucket(doc_vectors, query_vector, K):
	'''
	Identifying top-k relevant documents
	'''
	doc_score = dict()

	for doc_tag, doc_vector in doc_vectors.items():
		cos_score = unit_cosine_calc(doc_vector, query_vector)
		doc_score[doc_tag] = cos_score

	# Arranging dictionary as per score
	doc_bucket = [[x,doc_score[x]] for x in sorted(doc_score, key=doc_score.get, reverse=True)]

	if K > len(doc_bucket):
		return doc_bucket
	else:
		return doc_bucket[:(K+1)]

def query_vector_creation(incidence_mat, query, N):
	'''
	Imports existing vocab to creat tf-idf vector for query 
	'''
	query_terms = preprocessor(query)
	tf_vector = create_tf_vector(incidence_mat, query_terms)
	idf_vector = create_idf_vector(incidence_mat, N)
	tf_idf_vector = [x*y for x,y in zip(tf_vector, idf_vector)]
	unit_vector = convert_to_unit(tf_idf_vector)

	return unit_vector

def doc_similarity(doc_tag1, doc_tag2):
	'''
	Get cosine similarity between two docs present in the system
	'''
	doc_vectors = dict()
	doc_mappings = dict()
	cos_score = 0

	# loading doc vectors
	doc_vectors = read_from_json('data/doc_vectors.json')

	if doc_tag1 not in doc_vectors or doc_tag2 not in doc_vectors:
		print ('Invalid doc Tags :(')
	else:
		v1 = doc_vectors[doc_tag1]
		v2 = doc_vectors[doc_tag2]
		cos_score = unit_cosine_calc(v1, v2)
	
	return cos_score

def vs_relevancy(inp_sent, K=10):
	'''
	Interface for querying using vector space model
	'''
	incidence_mat = dict()
	doc_vectors = dict()

	# loading incidence matrix
	incidence_mat = read_from_json('data/incidence_matrix.json')
	
	# Ordering incidence matrix before vector creation, to have feature consistency in query
	incidence_mat = OrderedDict(sorted(incidence_mat.items()))

	# loading doc vectors
	doc_vectors = read_from_json('data/doc_vectors.json')

	# Total no of docs in the system
	N = len(doc_vectors)
		
	# Creating final query vector	
	query_vector = query_vector_creation(incidence_mat, inp_sent, N)

	# Getting k-most relevant docs
	k_bucket = relevant_K_bucket(doc_vectors, query_vector, K)

	return k_bucket