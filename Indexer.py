'''
Functions to create, edit and update index / incidence matrix
'''
import json
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
	Creates / Updates incidence matrix : {term:[df,{docid:tf,}]}
	'''
	for term in doc_words:
		if term in incidence_mat:
			# Term already exists
			# Add to document frequency
			incidence_mat[term][0] += 1

		else:
			# New term added
			incidence_mat[term] = [1,dict()]

		# Identifying document
		doc_stat = incidence_mat[term][1]

		if doc_id in doc_stat:
			# Document already exists
			doc_stat[doc_id] += 1
		else:
			# Add a new doc
			doc_stat[doc_id] = 1

		# Updating document stats
		incidence_mat[term][1] = doc_stat

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


def initialize(doc_list):
	'''
	Creates index, document mappings and vectors
	'''
	file_ext = ['.txt','.md']
	incidence_mat = dict()
	doc_mappings = dict()

	# Initiate indexing
	doc_mappings = create_mappings(doc_list)
	for document, doc_id in doc_mappings.items():
		
		# Check if it is a file
		if any([x in document for x in file_ext]):
			document = readfile(document)

		doc_words = linguistic_model(document)
		incidence_mat = incidence_update(incidence_mat, doc_id, doc_words)

	# Writing mappings on disk
	writejson('data/document_mappings.json',doc_mappings)

	# Writing incidnce matrix on disk
	writejson('data/incidence_matrix.json',incidence_mat)

	print ('Index & Mappings successfully created/updated :)')


if __name__ == '__main__':
	documents = ['test/test3.txt',"Hiya, Even this would work well"]
	# Can enter both files and text in this function
	initialize(documents)