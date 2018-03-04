'''
Functions to create, edit and update index / incidence matrix
'''
import copy
from collections import OrderedDict
from .linguistics import preprocessor
from .files import write_to_json, read_to_string, read_from_json
from .vectoropt import create_tf_vector, convert_to_unit

def incidence_matrix_creator(doc_terms):
	'''
	Creates incidence matrix : {term : {doc_tag : freq of term in doc}}
	doc_terms is a dictionary containing {doc_tag : words in doc}
	'''
	incidence_mat = dict()
	
	for tag, terms in doc_terms.items():
		for term in terms:
			if term not in incidence_mat:
				# New term added
				incidence_mat[term] = dict()

			# Identifying doc
			doc_stat = incidence_mat[term]

			if tag in doc_stat:
				# doc already exists
				doc_stat[tag] += 1
			else:
				# Add a new doc
				doc_stat[tag] = 1

			# Updating doc stats
			incidence_mat[term] = doc_stat

	# Ordering incidence matrix to maintain consistency
	incidence_mat = OrderedDict(sorted(incidence_mat.items()))

	return incidence_mat

def vs_fit(train_data, train_target, init=True):
	'''
	Creates incidence matrix, doc features and vectors
	if init is made False then it starts storing and loading previous training material
	'''
	incidence_mat = dict()
	doc_terms = dict()
	doc_vectors = dict()
	tagged_docs = {'data':list(), 'target':list()}

	if not init:
		# Loading previously stored data, if exists
		data = read_from_json('data/tagged_docs.json')
		if isinstance(data, dict):
			tagged_docs = data

	# Accumulating training material together
	for data, target in zip(train_data, train_target):
		if target in tagged_docs['target']:
			tgt_index = tagged_docs['target'].index(target)
			
			# Append doc with a space
			tagged_docs['data'][tgt_index] += ' ' + data
		else:
			# Append both as new entries
			tagged_docs['data'].append(data)
			tagged_docs['target'].append(target)

	# Processing accumulated data
	for data, target in zip(tagged_docs['data'], tagged_docs['target']):

		# Preprocessing doc into collection of words
		cleansed_words = preprocessor(data)

		# Adding cleansed words as terms for doc
		if target in doc_terms:
			doc_terms[target].extend(cleansed_words)
		else:
			doc_terms[target] = cleansed_words

	# Creating incidence matrix from doc features
	incidence_mat = incidence_matrix_creator(doc_terms)

	# Creating feature vector for docs in the system
	for tag, terms in doc_terms.items():
		tf_vector = create_tf_vector(incidence_mat, terms)
		unit_vector = convert_to_unit(tf_vector)
		doc_vectors[tag] = unit_vector

	# Writing existing tagged documents on disk
	write_to_json(tagged_docs, 'data/tagged_docs.json')

	# Writing doc vectors on disk
	write_to_json(doc_vectors, 'data/doc_vectors.json')

	# Writing doc features on disk
	write_to_json(doc_terms, 'data/doc_features.json')

	# Writing incidnce matrix on disk
	write_to_json(incidence_mat, 'data/incidence_matrix.json')

	print ('Model Training Complete :)')