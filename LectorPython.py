import json

with open ('fichero.txt') as json_file:
	data = json.load(json_file)



	s = data['n_orig']
	print (data)
