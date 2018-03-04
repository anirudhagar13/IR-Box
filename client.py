# How to Use IRBox

from DocRetriever import vs_fit, vs_relevancy, doc_similarity

# ~ Initialized with a set of documents tagged with their respective classes
data = ['This shirt is amazing.','I hate my job.','That hairstyle is moderately good.','I am good at procrastinating.']
target = ['pos','neg','neu','pos']

# ~ Initializing System
vs_fit(data, target)

# ~ After system has been initialized

# ~ Comparing two documents with each other
# sim_score = doc_similarity('pos', 'neu')
# print ('Similarity between documents : ', sim_score)

# ~ Query client
# while True:
# 	inp_sent = input("\nEnter your Query. Press 'e' to exit : \n>> ")
# 	if inp_sent == 'e':
# 		break

# 	relevant_docs = vs_relevancy(inp_sent)
# 	print ('\nFollowing are documents in decreasing order of relevance : \n>>', relevant_docs)