# Contains re-usable file related operations
import json
import pickle
import os

dirpath = os.path.dirname(__file__)
if dirpath:
	# To compensate relative paths
	dirpath += '/'

def read_to_string(inpfile_path):
	'''
	Function that returns content of a file in a string
	'''
	data = ''
	inpfile_path = dirpath + inpfile_path
	try:
		with open(inpfile_path, 'r') as inp_file:
			data = inp_file.read().replace('\n', ' ')
	except Exception as e:
		print ("'read_to_string' - Issue with file : ",e)

	return data

def read_from_json(inpfile_path):
	'''
	Reads json file and return data
	'''
	data = dict()
	inpfile_path = dirpath + inpfile_path
	try:
		with open(inpfile_path,'r') as inpfile:
			data = json.load(inpfile)
	except Exception as e:
		print ("'read_from_json' - Issue with file : ",e)

	return data

def write_to_json(data, outfile_path):
 	'''
 	Dumps data into json file, data should be a formattable json
 	'''
 	outfile_path = dirpath + outfile_path

 	try:
 		with open(outfile_path,'w') as outfile:
	 		json.dump(data, outfile, indent=4)
 	except Exception as e:
 		print ("'write_to_json' - Issue with file : ",e)	