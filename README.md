# IR-Engine
A python based IR retrieval system that leverages vector space model and TF-IDF

~ Dependencies:
	- Python3
	- NLTK
	- Spacy
	- spacy en model

~ Functionality:
	- Creates index and vectors for documents when initialized
	- When searching for query, it uses already created index to give top-k relevancy answer 
	- Uses tf-idf score as weights in vector space model
	- Run client.py file to interact with the system. Uncommenet whatever functionality that needs to be used.

~ Features:
	- Query search = returns most relevant documents in k-bucket size of which can be altered
	- Document comparison = Can compare how similar two documents are residing in the system
	- Dynamic documents addtion = Can add list of documentsin already indexed system
	- Dynamic document deletion = Can delete list of documents from already indexed system