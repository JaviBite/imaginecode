import json

with open ('fichero.json') as json_file:
	data = json.load(json_file)



	s = data['n_orig']
	print (data)
