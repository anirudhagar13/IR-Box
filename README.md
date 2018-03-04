# IR-Box / Document Retriever
A basic python based IR retrieval system that leverages vector space model and TF-IDF

~ Dependencies:
	- Python3
	- NLTK
	- Spacy
	- spacy en model

~ Info:
	- Based on (https://www.youtube.com/watch?v=PhunzHqhKoQ) by Dan Jurafsky
	- View client.py to check its interface
	- The system does not uses TFIDFVectorizer coz I didn't know about it when I created this
	- Also, pre-processing while fitting and predicting involves lemmatization, hence the system is really slow

~ Features:
	- Query search = returns most relevant documents in k-bucket, size of which can be altered by passing parameter (K=integer) in 'vs_relevancy()' while querying
	- Document comparison = Can compare how similar two documents are residing in the system
	- Dynamic documents addtion = pass parameter (init=False) in 'vs_fit()' and it will append documents to already existing index