#!flask/bin/python
from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import MySQLdb
import requests

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "api physlogic"
@app.route('/make_task', methods=["POST"])
def start():
	authorized = requests.get('http://149.154.64.47:5001/checkapp', {"ip": request.remote_addr})
	
	if authorized.text == '1':
		print(authorized.text)
		json_data = json.loads(request.json)
		have = []
		need = []
		for j in json_data["have"][0]:
			have.append(j) # key
		for i in json_data["find"]:
			need.append(i) #key to find
		result = str(json.dumps(solution(need, have)))
		print(result)
		return(result)
	else:
		return("You ne avtorizirovan, kogo reshil naebat'?")


def solution(find, have):
	toreturnmass = []
	for i in find:
		math_symbols = '+-*/^)( '
		testlevel = 0
		buffered = ''
		#parsing
		stringvar = '(' + i + ')' # converting to string
		numberofsymbol = 0
		while numberofsymbol < len(stringvar):
			for k in math_symbols: #check compliance
				if (stringvar[numberofsymbol] == k):
					
					if buffered != '': #if buffer is not empty
						
						if have.count(buffered) > 0: #make check in "have"
							
							buffered = ''
							testlevel = 0
							
						else:
							formul = getBD(buffered)
							print(formul)
							if len(formul) != 0: # check for null value
								stringvar = stringvar.replace(str(buffered), "(" + str(formul[0][1]) + ")")
								numberofsymbol -= len(buffered)
								buffered = ''
								testlevel = 0
					buffered = ''
					testlevel = 0
					numberofsymbol += 1
					break
				else:
					testlevel += 1
				if testlevel == len(math_symbols):
					buffered += stringvar[numberofsymbol] #if symbol not equal math sign - append symbol to buffer
					print(buffered, stringvar[numberofsymbol], '1')
					testlevel = 0 
					numberofsymbol += 1
					break


		#append
		toreturnmass.append(stringvar)
	return(toreturnmass)
def getBD(variable):
	sql = "SELECT head , body , theme FROM tasks WHERE head='%s'" % variable
	file = open('password')
	password = file.read()
	db = MySQLdb.connect(host="localhost", user="root", passwd=password, db="physlogic", charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)
	return(cursor.fetchall())

if __name__ == '__main__':
    app.run(debug=True,host='149.154.64.47')
