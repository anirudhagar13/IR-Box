import spacy

class SWrapper:
	'''
	A class to encapsulate all functionalities that can be exploited from spacy linguistics
	'''
	inp_sent = ''
	doc = object()	# Empty object to store processed sentence

	def __init__(self, inp_sent):
		'''
		Initializing inp sentence inside constructor
		'''
		self.inp_sent = inp_sent

		# Processing sentence
		en_nlp = spacy.load('en')
		self.doc = en_nlp(inp_sent)

	def __str__(self):
		'''
		prints this object
		'''
		return self.inp_sent

	def get_pos(self):
		'''
		returns superficial pos tags as [[word, tag]...]
		'''
		pos = list()
		for token in self.doc:
			temp = list()
			temp.append(token.text)
			temp.append(token.pos_)
			pos.append(temp)

		return pos

	def get_lemmas(self):
		'''
		returns a list of tokens in the sentence in their basic form
		'''
		lemmas = list()
		for token in self.doc:
			temp = list()
			temp.append(token.text)
			temp.append(token.lemma_)
			lemmas.append(temp)

		return lemmas

	def get_entities(self):
		'''
		returns list of tags with thier entity labesl as [[word, label]...]
		'''
		labels = list()
		for token in self.doc.ents:
			temp = list()
			temp.append(token.text)
			temp.append(token.label_)
			labels.append(temp)

		return labels

	def get_noun_phrases(self):
		'''
		returns all noun phrases
		'''
		return list(self.doc.noun_chunks)

	def get_tags(self):
		'''
		returns detailed pos tags as [[word, tag]...]
		'''
		tag = list()
		for token in self.doc:
			temp = list()
			temp.append(token.text)
			temp.append(token.tag_)
			tag.append(temp)

		return tag

	def get_dependency(self):
		'''
		Returns dependency in format [[relation, governor, dependent]...]
		'''
		dependencies = list()
		for token in self.doc:
			temp = list()
			temp.append(token.dep_)	# adding relation
			temp.append(token.head.text) # adding governor/head
			temp.append(token.text) # adding dependent
			dependencies.append(temp)

		return dependencies

	def is_alpha(self):
		'''
		returns if word is alpha numeric or not [[word, is_alpha]...]
		'''
		is_alpha = list()
		for token in self.doc:
			temp = list()
			temp.append(token.text)
			temp.append(token.is_alpha)
			is_alpha.append(temp)

		return is_alpha

	def is_stop(self):
		'''
		returns if word is stop word or not [[word, is_stop]...]
		'''
		is_stop = list()
		for token in self.doc:
			temp = list()
			temp.append(token.text)
			temp.append(token.is_stop)
			is_stop.append(temp)

		return is_stop

if __name__ == '__main__':
	inp_sent = input('Enter Input Sentence for Dependency Parsing : \n >> ')

	spacy_obj = SWrapper(inp_sent)
	# print (spacy_obj)
	# print (spacy_obj.get_dependency())
	# print (spacy_obj.get_entities())
	# print (spacy_obj.get_noun_phrases())
	# print (spacy_obj.get_pos())
	# print (spacy_obj.get_tags())
	# print (spacy_obj.get_lemmas())
	# print (spacy_obj.is_alpha())
	# print (spacy_obj.is_stop())