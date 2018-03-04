# Contains various language related operations
# Its dependency is spacywrapper.py and nltk

from .spacywrapper import SWrapper
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
Stopwords = set(stopwords.words('english'))

def preprocessor(document):
	'''
	Performs the following operations and returns a list of cleansed words
	1. Reduces to lower case
	2. Removes certain symbols
	3. Replace certain symbols
	4. Removes stop words and non-alphanumerics
	4. Lemmatizes words into basic form
	'''
	cleaned_words = list()

	# Reduce to lower case
	document = document.lower()

	# Removing forbidden items
	forbidden_list = ["'s","-",","]
	for x in forbidden_list:
		if x in document:
			document = document.replace(x,'')

	# Replace items with space
	replace_list = ["_"]
	for x in replace_list:
		if x in document:
			document = document.replace(x,' ')

	sentences = sent_tokenize(document)
	for inp_sent in sentences:
		temp = list()
		spacy_obj = SWrapper(inp_sent)

		# Remove stop words, non-alphanumerics and words less than length 2
		temp = [x[0] for x in spacy_obj.is_alpha() if x[1] == True and len(x[0]) > 2 and x[0] not in Stopwords]

		# Reduce to lemma
		cleaned_words.extend([x[1] for x in spacy_obj.get_lemmas() if x[0] in temp])

	return cleaned_words