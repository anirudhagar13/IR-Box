'''
Functions to create, edit and update index / incidence matrix
'''
import json
import copy
from vectoropt import *
from spacywrapper import SWrapper
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
Stopwords = set(stopwords.words('english'))


def linguistic_model(document):
	'''
	All Language processing happens here
	'''
	cleaned_words = list()

	# Reduce to lower case
	document = document.lower()

	# Removing forbidden items
	forbidden_list = ["'s","-",","]
	for x in forbidden_list:
		if x in document:
			document = document.replace(x,'')

	sentences = sent_tokenize(document)
	for inp_sent in sentences:
		temp = list()
		spacy_obj = SWrapper(inp_sent)

		# Remove stop words, non-alphanumerics and words less than length 2
		temp = [x[0] for x in spacy_obj.is_alpha() if x[1] == True and len(x[0]) > 2 and x[0] not in Stopwords]

		# Reduce to lemma
		cleaned_words.extend([x[1] for x in spacy_obj.get_lemmas() if x[0] in temp])

	return cleaned_words

def incidence_update(incidence_mat, doc_id, doc_words):
	'''
	Creates / Updates incidence matrix : {term:{docid:tf,}}
	'''
	for term in doc_words:
		if term not in incidence_mat:
			# New term added
			incidence_mat[term] = dict()

		# Identifying document
		doc_stat = incidence_mat[term]

		if doc_id in doc_stat:
			# Document already exists
			doc_stat[doc_id] += 1
		else:
			# Add a new doc
			doc_stat[doc_id] = 1

		# Updating document stats
		incidence_mat[term] = doc_stat

	return incidence_mat

def readfile(filename):
	'''
	Function that returns content of a file in a string
	'''
	with open(filename, 'r') as inp_file:
		data = inp_file.read().replace('\n', ' ')

	return data

def writejson(outfile_name, data):
 	'''
 	Dumps data into json file
 	'''
 	with open(outfile_name,'w') as outfile:
 		json.dump(data, outfile, indent=4)

def create_mappings(doc_list):
	'''
	Accepts document file names / text and creates a mapping with an alias
	'''
	doc_mappings = dict()

	for index, doc in enumerate(doc_list):
		
		# Each doc aliased by a doc Id, as DOC#
		doc_mappings[doc] = 'DOC' + str(index)

	return doc_mappings

def init_engine(doc_list):
	'''
	Creates index, document mappings and vectors
	'''
	file_ext = ['.txt','.md']
	incidence_mat = dict()
	doc_mappings = dict()
	doc_vectors = dict()

	# Initiate indexing
	doc_mappings = create_mappings(doc_list)
	for document, doc_id in doc_mappings.items():
		
		# Check if it is a file
		if any([x in document for x in file_ext]):
			document = readfile(document)

		doc_words = linguistic_model(document)
		# Adding to doc_vectors to be used later while creating vectors 
		doc_vectors[doc_id] = doc_words

		# Incidence Matrix creation
		incidence_mat = incidence_update(incidence_mat, doc_id, doc_words)

	# Creating vectors for documents in the system
	temp = copy.deepcopy(doc_vectors)
	for doc_id, doc_words in temp.items():
		tf_vector = create_tf_vector(incidence_mat, doc_words)
		unit_vector = convert_to_unit(tf_vector)
		doc_vectors[doc_id] = unit_vector

	# Writing mappings on disk
	writejson('data/document_mappings.json',doc_mappings)

	# Writing vectors on disk
	writejson('data/document_vectors.json',doc_vectors)

	# Writing incidnce matrix on disk
	writejson('data/incidence_matrix.json',incidence_mat)

	print ('Index, Vectors & Mappings successfully created/updated :)')


if __name__ == '__main__':
	# Can enter both files and text in this function
	documents = ['Hey, what is happening?',"Is this really going to happen?"]
	init_engine(documents)