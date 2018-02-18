import json
from collections import OrderedDict
from indexer import init_engine, linguistic_model
from vectoropt import *

def relevant_K_bucket(doc_vectors, query_vector, K):
	'''
	Identifying top-k relevant documents
	'''
	doc_score = dict()

	for doc_id, doc_vector in doc_vectors.items():
		cos_score = unit_cosine_calc(doc_vector, query_vector)
		doc_score[doc_id] = cos_score

	# Arranging list as per score
	doc_bucket = sorted(doc_score, key=doc_score.get, reverse=True)

	if K > len(doc_bucket):
		return doc_bucket
	else:
		return doc_bucket[:(K+1)]

def query_vector_creation(incidence_mat, query, N):
	'''
	Imports existing vocal and linguistic models to creat tf-idf vector for query 
	'''
	query_words = linguistic_model(query)
	tf_vector = create_tf_vector(incidence_mat, query_words)
	idf_vector = create_idf_vector(incidence_mat, N)
	tf_idf_vector = [x*y for x,y in zip(tf_vector, idf_vector)]
	unit_vector = convert_to_unit(tf_idf_vector)

	return unit_vector

def add_document(document):
	'''
	Adding new document to IR system. Can pe path to text file or text itself
	'''
	doc_mappings = dict()
	doc_list = list()

	# loading document mappings
	with open('data/document_mappings.json') as inpfile:
		doc_mappings = json.load(inpfile)

	doc_list.extend(doc_mappings.values())
	doc_list.append(document)

	# Updating the entire system
	init_engine(doc_list)

def del_document(doc_id):
	'''
	Enter doc_id to delete document
	'''
	doc_mappings = dict()

	# loading document mappings
	with open('data/document_mappings.json') as inpfile:
		doc_mappings = json.load(inpfile)

	if doc_id not in doc_mappings:
		print ('Invalid Document ID :(')
	else:
		doc_list = [doc_mappings[x] for x in doc_mappings.keys() if x != doc_id]

		# Updating the entire system
		init_engine(doc_list)

def compare_docs(doc_id1, doc_id2):
	'''
	Get cosine similarity between two documents present in the system
	'''
	doc_vectors = dict()

	# loading document vectors
	with open('data/document_vectors.json') as inpfile:
		doc_vectors = json.load(inpfile)

	if doc_id1 not in doc_vectors or doc_id2 not in doc_vectors:
		print ('Invalid Document IDs :(')
	else:
		v1 = doc_vectors[doc_id1]
		v2 = doc_vectors[doc_id2]
		cos_score = unit_cosine_calc(v1, v2)
		print ('\nSimilarity Metric between documents : ',cos_score,'\n')

def query_client():
	'''
	Interface for querying IR system
	'''
	incidence_mat = dict()
	doc_mappings = dict()
	doc_vectors = dict()

	# loading incidence matrix
	with open('data/incidence_matrix.json') as inpfile:
		incidence_mat = json.load(inpfile)
	
	# Ordering incidence matrix before vector creation
	incidence_mat = OrderedDict(sorted(incidence_mat.items()))

	# loading document mappings
	with open('data/document_mappings.json') as inpfile:
		doc_mappings = json.load(inpfile)

	# loading document vectors
	with open('data/document_vectors.json') as inpfile:
		doc_vectors = json.load(inpfile)

	# Total no of docs in the system
	N = len(doc_mappings)

	while True:
		inp_sent = input("\nEnter your Query. Press 'e' to exit : \n>> ")
		if inp_sent == 'e':
			break

		# Creating final query vector	
		query_vector = query_vector_creation(incidence_mat, inp_sent, N)
		k_bucket = relevant_K_bucket(doc_vectors, query_vector, 10)
		
		# Getting actual documents from doc_ids in decreasing order of relevance
		relevant_docs = [doc_mappings[x] for x in k_bucket]
		print ('\nFollowing are documents in decreasing order of relevance : \n>>', relevant_docs)


if __name__ == '__main__':
	# -> To initialize IR System.

	# Can give here a list containing path of text files / texts as documents
	# documents = ['test/test1.txt','test/test2.txt','test/test3.txt',"Is this really going to happen bhai?"]
	# init_engine(documents)

	# -> After initializing IR System

	# To add new doc to the system
	# add_document('test/test4.txt')

	# To del a doc from system using doc_id
	# del_document('DOC4')

	# To compare similaity between two docs using doc_ids
	# compare_docs('DOC4','DOC1')
	
	# To query System
	# query_client()