import sys

sys.setrecursionlimit(1 << 30)

#--------------<Built-in Functions>--------------

adder			= lambda x,y:x+y
subtract		= lambda x,y:x-y
multiply		= lambda x,y:x*y
divide			= lambda x,y:x/y
integerer		= lambda x:int(x)
floater			= lambda x:float(x)
minusOne		= lambda x:x-1
plusOne			= lambda x:x+1
square			= lambda x:x**2
compare			= lambda x,y:int(x==y)
lesserThan		= lambda x,y:int(x<y)
greaterThan		= lambda x,y:int(x>y)
printer			= lambda x:print(str(x).replace('/n','\n'))
ander			= lambda x,y:int(x and y)
orer			= lambda x,y:int(x or y)
moder			= lambda x,y:x%y
doubler			= lambda x:2*x
halver			= lambda x:x/2

dictionary={
	'~':{'func':minusOne,'args':1},
	';':{'func':plusOne,'args':1},
	'D':{'func':doubler,'args':1},
	'H':{'func':halver,'args':1},
	'+':{'func':adder,'args':2},
	'-':{'func':subtract,'args':2},
	'*':{'func':multiply,'args':2},
	'/':{'func':divide,'args':2},
	"I":{'func':integerer,'args':1},
	"F":{'func':floater,'args':1},
	'%':{'func':moder,'args':2},
	'S':{'func':square,'args':1},
	'<':{'func':lesserThan,'args':2},
	'>':{'func':greaterThan,'args':2},
	'=':{'func':compare,'args':2},
	'&':{'func':ander,'args':2},
	'|':{'func':orer,'args':2},
	'P':{'func':printer,'args':1}
}

#--------------<Built-in Functions/>-------------

def atomicInterpret(func,arguments):
	if len(arguments)==1:return dictionary[func]['func'](arguments[0])
	if len(arguments)==2:return dictionary[func]['func'](arguments[0],arguments[1])
 
def tokenizer(statement):
	tokens,i,j=[],0,0
	while i<len(statement):
		token=statement[i]
		if token in '0123456789.':
			j=1
			while i+j<len(statement)and statement[i+j]in '0123456789.':
				token+=statement[i+j];j+=1
			i+=j;tokens+=[token]
		elif token=='"':
			j=1
			token=''
			while i+j<len(statement)and statement[i+j]!='"':
				token+=statement[i+j];j+=1
			i+=j+1;tokens+=["'"+token+"'"]
		elif token=="'":
			j=1
			token=''
			while i+j<len(statement)and statement[i+j]!="'":
				token+=statement[i+j];j+=1
			i+=j+1;tokens+=["'"+token+"'"]
		elif token=='[':
			j=1
			token=''
			while i+j<len(statement)and statement[i+j]!=']':
				token+=statement[i+j];j+=1
			i+=j+1;tokens+=['['+token+']']
		elif token==' 'or token=='	':
			i+=1
		elif token=='-':
			j=1
			while i+j<len(statement)and statement[i+j]in '0123456789.':
				token+=statement[i+j];j+=1
			i+=j
			tokens+=[token]
		else:
			i+=1
			tokens+=[token]
	return tokens

def evaluate(expression):
	operandStack=[]
	for token in tokenizer(expression)[::-1]:
		if token in dictionary.keys():
			if len(operandStack)<dictionary[token]['args']:raise Exception
			operands=[]
			argsLeft = dictionary[token]['args']
			while argsLeft:
				operands.append(eval(operandStack.pop()))
				argsLeft-=1
			calc=atomicInterpret(token,operands)
			if type(calc)==type(""):operandStack.append("'"+calc+"'")
			else:operandStack.append(str(calc))
		else:
			operandStack.append(token)
	result = eval(operandStack.pop())
	if operandStack:
		raise Exception
	return result

def function_interpret(function_statement):
	function_string = function_statement.split('@')[0]
	arguments_string = function_statement.split('@')[1]
	arguments = arguments_string.split()
	compiled = tokenizer(function_string)
	alphas=[i for i in compiled if len(i)==1 and 'a'<=i<='z']
	if alphas:
		start_alpha=min(alphas)
		for i,x in enumerate(compiled):
			if len(x)==1 and 'a'<=x<='z':compiled[i]=' '+str(interpret(arguments[ord(x)-ord(start_alpha)]))+' '
	compiled=''.join(compiled)
	try:
		return str(interpret(compiled))
	except:
		#probably is recursive, lets reduce it
		recursive=compiled.count('$')*['']
		compiled_inverted= compiled[::-1]
		i=0
		for n,x in enumerate(recursive):
			while compiled_inverted[i]!='$':i+=1 
			recursive[n]='$';i+=1
			while compiled_inverted[i]!='#':recursive[n]=compiled_inverted[i]+recursive[n];i+=1
			recursived=str(interpret(recursive[n][:-1]))
			compiled = compiled.replace('#'+recursive[n], ' '+str(interpret(function_string+'@'+recursived))+' ')
		return str(interpret(compiled)) 

def interpret(statement):
	try:
		if '@' in statement:
			return function_interpret(statement)
		if ':' in statement:
			condition=statement[:statement.find(':')]
			statements=statement[statement.find(':')+1:]
			statements_inverted=statements[::-1]
			if_statement=statements_inverted[statements_inverted.find('!')+1:][::-1]
			else_statement=statements_inverted[:statements_inverted.find('!')][::-1]
			if interpret(condition):return interpret(if_statement)
			if (else_statement):return interpret(else_statement)
			else:return None
		else:
			return evaluate(statement)
	except:
		raise Exception

#Behaves as an REPL
if len(sys.argv)==1:
	while 1:
		inString=input(">> ")
		if inString=="q":break;
		try:
			outPut=interpret(inString)
			if str(outPut)!='None':print('=> '+str(outPut))
		except:print("=> Error!")
	exit()

#Read code and inputs from file
try:
	code=inputted=''
	code_file_path = sys.argv[1]
	with open(code_file_path) as code_file:
		for row in code_file:
			code=row
	code_file.close()
	if len(sys.argv)==3:
		input_file_path = sys.argv[2]
		with open(input_file_path) as input_file:
			for row in input_file:
				inputted=row
		input_file.close()
		if inputted:code+='@'+inputted
	outPut=interpret(code)
	if str(outPut)!='None':print(str(outPut))
except:print("Error!")