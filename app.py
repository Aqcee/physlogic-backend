#!flask/bin/python
from flask import Flask, request
import json
import MySQLdb
app = Flask(__name__)
@app.route('/')
def index():
    return "api physlogic"
@app.route('/make_task', methods=["POST"])
def start():
	json_data = json.loads(request.json)
	sqlreq = "SELECT head , body , theme FROM tasks WHERE head='%s'" % json_data["find"][0]
	have = []
	need = []
	figurehave = []
	courseofsolition = []
	for j in json_data["have"][0]:
		have.append(j)
	for k in json_data["have"][1]:
		figurehave.append(k)
	for i in json_data["find"]:
		need.append(i)
	massform = findFormul(sqlreq, need, have)
	final = replacer(massform, need[0], have, figurehave)
	figuredformul = make(need[0], json_data, final)
	courseofsolition.append(final)
	courseofsolition.append(figuredformul)
	return(str(courseofsolition))
def make(find, json_data, formul):
	formulString = find+"="+formul
	formulMassive=[]
	operands='-+/*()^='
	bufferVar=''
	for symbol in formulString:
		if(operands.find(symbol)==-1):
			bufferVar = bufferVar + symbol
		if(operands.find(symbol)!=-1):
			formulMassive.append(bufferVar)
			bufferVar=''
			formulMassive.append(symbol)
	formulMassive.append(bufferVar)
	numberInsteadCharsInFormul=""
	alreadyAdded = False
	for symbol in formulMassive:
		for i in range(len(json_data["have"][0])):
			if (symbol == json_data["have"][0][i-1]):
				numberInsteadCharsInFormul = numberInsteadCharsInFormul + json_data["have"][1][i-1]
				alreadyAdded = True
				break
		if (symbol != json_data["have"][0][i-1] and alreadyAdded == False):
			numberInsteadCharsInFormul = numberInsteadCharsInFormul + symbol
			alreadyAdded = True
		alreadyAdded = False
	return(numberInsteadCharsInFormul)
def mathReactor(expression):
	expressionRefact = ""
	numberList = ['0','1','2','3','4','5','6','7','8','9']
	operandsList= ['-','+','/','*','(',')','^']
	bufferVar = ''
	for symbol in expression:
		for operand in operandsList:
			if (symbol==operand):
				expressionRefact = expressionRefact+operand
				break
			
		for number in numberList:
			if (symbol == number):
				bufferVar = bufferVar + symbol
				expressionRefact = expressionRefact + number
				break
	answer = eval(expressionRefact)			
	return(answer)
def replacer(Formulas, stringIn, have, figurehave):
	math = ['/', '+', '-', '*', '(', ')', ' ']
	i = 0
	testlevel = 0
	buffered = ''
	final = ''
	while True:
		if final == '':
			final = str(stringIn)
		if i == len(final):
			break
		for j in math:
			if j != final[i]:
				testlevel+=1
			if testlevel == len(math):
				buffered = buffered + final[i]
				testlevel = 0
				break
		toreplace = ''
		k = 0
		while k < len(Formulas):
			if Formulas[k] == buffered:
				toreplace = Formulas[k+1]
			k+=2
		if toreplace != '':
			final = final.replace(buffered, toreplace)
			i = -1
			buffered = ''
		else:
			if have.count(buffered) == 1:
				buffered = ''
		i+=1
		print(final, i, buffered, toreplace)
	return(final)
final = []
iteration = 0
def findFormul(dbreq, need, have):
	formula = reqDB(dbreq)
	print(dbreq)
	if formula[0][2] == 'const':
		final.append(formula[0][0])
		final.append(formula[0][1])
		return(final)
	needed = parsing(formula[0][1])
	global iteration
	for i in needed[0]:
		check = haveexist(i, have)
		print(check)
		print(needed[0])
		if check[0] != 0:
			iteration+=1
			if iteration == needed[1]:
				final.append(formula[0][0])
				final.append(formula[0][1])
				iteration = 0
		else:
			iteration+=1
			if iteration == needed[1]:
				final.append(formula[0][0])
				final.append(formula[0][1])
				iteration = 0
			tradebuffer = iteration
			iteration = 0
			per = findFormul("SELECT head , body , theme FROM tasks WHERE head='%s'" % check[1], check[1],have)
			iteration = tradebuffer
	return(final)
def reqDB(sql):
	file = open('password')
	password = file.read()
	db = MySQLdb.connect(host="localhost", user="root", passwd=password, db="physlogic", charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)
	return(cursor.fetchall())	
def haveexist(need, have):
	testlevel = 0
	ite = 0
	for j in have:
		if ite >= len(have):
			ite = 0
		if need == j: 
			return(1, have[ite])
		else:
			testlevel += 1
		if testlevel>=len(have):
			return(0, need)
		ite+=1
def parsing(formula):
	math_signs = ['-','+','*','/', '^', '>', '1','2','3','4','5','6','7','8','9','0']
	symbol = 0
	symbolformul = list(formula)
	nextsymbol = 0
	variables = []
	testlevel = 0
	variable = ''
	j = 0
	returned = []
	number = 0 
	while True:
		if (j==len(symbolformul)):
			variables.append(variable)
			number+=1
			break
		for i in math_signs:
			if i == symbolformul[j]:
				variables.append(variable)
				variable = ''
				testlevel = 0
				number+=1
				break
			else: 
				testlevel += 1
				if testlevel == len(math_signs):
					variable += '' + symbolformul[j]
					testlevel = 0
					break
		j += 1
	for i in variables: 
		if i != '':
			returned.append(i.lower())
	return(returned, number)
if __name__ == '__main__':
    app.run(debug=True,host='149.154.64.47')