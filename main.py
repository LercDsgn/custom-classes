options = {"allowMultipleWordNames":{"all":True}, "errors":{"createClass":{"typeConversion":{ "dictToList": True, "strToList": True, "intToStrToList": True }}},  # maybe dont check any if all of it is false in createClass definition
"allowMultipleParents": False, "goWithBestMatch": False, "silenceOnDuplicateKey": False, "defaultObjectParentToSingleExistingClass": False}

def getKey(val, testdict):
    for key, value in testdict.items():
         if val == value:
             return key
 
    return "key doesn't exist"


def sinplu(variable, singular="", plural="s"): return singular if variable == 1 else plural 
def defaultInitConsoleOutput(name): return f"class <{name}> created successfully"
def bestMatch(text, matches): 
	maximum = ["",0]
	score = 0

	for i in matches:
		for n, j in enumerate(i):
			score = 0
			if j in text:
				score += 1
				if n < len(text) and j == text[n]:
					score += 1

		if score > maximum[1]:
			maximum = [i, score]
	return maximum[0]

#print(bestMatch("hello", ["haslo", "haolo", "hullo", "hello"]))
"""
def easdfkm(e, text, args, inherits, classes):
	e[text] = (args + [i for i in classes[inherits][text] if i not in secretArgs]) if inherits else args
"""

classes = {}

def prettyprintClasses(classes = classes):
	print()								
	for i in classes.keys():
		
		print(f"{i} ({len(classes[i]['objects'])})")
		#print("-"*len(i))
		for n, i in enumerate(classes[i]["objects"]):
			print("-"*(len(i)+1), n+1, "-", i)
		print("\n")

# ---------------- bool return
def hasParent(name, classes=classes):
	for i in classes.keys():
		if name in classes[i]["objects"]: return i
	return False
def classExists(name, classes = classes): 									return name in classes.keys()
def argsValid(name, args: dict, classes = classes): 						return list(args.keys()) == getArgs(name)
def argsLengthValid(name, args: dict, classes = classes):					return len(args.keys()) == len(getArgs(name))
# ---------------- string return
def getParent(name:str): 
	for i in classes.keys(): 
		if name in classes[i]["objects"]: return i
def getAllParents(name:str): [i for i in classes.keys() if name in classes[i]["objects"]]  #global option: allowMultipleParents  
def getAllClasses(classes = classes): 										return list(classes.keys())
def getClass(name, classes = classes): 									
	if name in classes: return classes[name]
	else: raise NameError(f"Class '{name}' doesn't exist!")
def getArgs(name, custom = True, init = False, classes = classes): 			return (list(getClass(name)["customArgs"]) if custom else []) + (getClass(name)["initArgs"].keys() if init else []) #return [i for i in (list(getClass(name)["customArgs"]) if custom else []) + (getClass(name)["initArgs"].keys() if init else []) if i not in getClass(name)["secretArgs"]]
def getObjects(name, classes = classes, details = False):					return getClass(name)['objects'] if details else list(getClass(name)['objects'].keys())
def getAllObjects(showEmpty = True, details = False): 						return [{i : classes[i]['objects'] if details else list(classes[i]['objects'].keys()) } for i in classes.keys()]
def getObject(parent, name, classes = classes, details=False):				return getObjects(parent, details=True)[name] if details else list(getObjects(parent, details=True)[name].keys())# ( = get object arguments)
def getNumberOfObjects(name, classes = classes): 	      					return len(getObjects(className))
def getArgValue(parent, name, arg): 
	if (arg not in getClass(parent)["secretArgs"]): # or "silenceOption": #todo 
		return getClass(parent)["objects"][name][arg] 
	else:
		raise SyntaxError(f"Can't access secret argument '{name}'")


# ----------------- do-ers
def createClass(name:str, customArgs:list = [], initArgs:dict = {}, secretArgs = [], constantArgs = [], onNewObject = lambda: "", onNewInheritedClass = lambda: "", initConsoleOutput:str = None, inherits = None):
	if inherits is not None and inherits not in classes: 
		if "silenceOptionHere":
			raise NameError(f"No class named '{inherits}'")
	conv = options["errors"]["createClass"]["typeConversion"]
	customArgs = list(customArgs.keys() if conv["dictKeys"] else customArgs.values()) if type(customArgs) == dict and conv["dictToList"] else customArgs
	customArgs = [str(customArgs)] if type(customArgs) == int and conv["intToStrToList"] else customArgs
	customArgs = [customArgs] if type(customArgs) == str and conv["strToList"] else customArgs #initArgs.split() if type(initArgs) == str --> this approach doesnt work with long named arguments 
	classes[name] = {"parent": inherits or None, "customArgDefaults": [{i: initArgs[i]} for i in customArgs if i in initArgs], 
	"initArgs": ([{i: initArgs[İ]} for i in initArgs if i not in customArgs] + [i for i in classes[inherits]["initArgs"] if i not in initArgs]) if inherits else initArgs, 
	"customArgs": ([i for i in customArgs if i not in initArgs] + [i for i in classes[inherits]["customArgs"] if i not in customArgs]) if inherits else customArgs, 
	"secretArgs": (secretArgs + [i for i in classes[inherits]["secretArgs"] if i not in secretArgs]) if inherits else secretArgs,
	"constantArgs": (constantArgs + [i for i in classes[inherits]["secretArgs"] if i not in secretArgs]) if inherits else secretArgs,
	"onNewObject": onNewObject, "objects":{},
	"history":{} # add time based history? #TODO
	}
	initConsoleOutput = initConsoleOutput or defaultInitConsoleOutput(name)
	#print(initConsoleOutput)
	return name

def deactivateClass(name:str):
	if classExists:
		classes[name]["active"] = False
def deleteClass(name:str):
	if classExists:
		del classes[name]
	else:
		raise NameError(f"No class named {name}")
def renameClass(name:str, newName:str):
	if classExists:
		classes[newName] = classes[name]
		del classes[name]
	else:
		raise NameError(f"No class named {name}")

def guessParent():
		if options["defaultObjectParentToSingleExistingClass"]: 
			if len(classes) == 1: return list(classes.keys())[0] # if only one class exists, parent is that class
			else: raise TypeError(f"Parent for object {name} isn't specified and can't default, because more than one class exists.")
		else:
			raise TypeError(f"Parent for object {name} isn't specified")
	
def createObject(name:str, parent = None, args:dict = {}):
	parent = parent or guessParent() 
	# put checks in order specific to general 
	checks = [ (classExists(parent)), (argsValid(parent, args)), (argsLengthValid(parent,args)),  (name not in getObjects(parent) or options["silenceOnDuplicateKey"]), ((not hasParent(name)) and not options["allowMultipleParents"])]
	if all(checks):
		x = {**classes[parent]['initArgs'], **args}
		getObjects(parent, details=True)[name] = x # LOOK: WHY DOESN'T getObject(parent, name) work here? ||||||||||| also considered: { object / args / [arg1, arg2, ...] } instead of { object / [arg1, arg2...]}
		getClass(parent)["onNewObject"]()
		return name if "option" else x
	if all(checks[:-1]):
		print(checks)
		error = f"Object '{name}' can't be created for class '{parent}' as it already exists for class '{getParent(name)}'."
		raise TypeError(error)
	if all(checks[:-2]):
		raise TypeError(f"Object '{name}' of class '{parent}' already exists!")	
	if all(checks[:-3]): # args invalid
		#error = f"Keys: '{args.keys()}', Keys2: '{getArgs(parent)}',  Class '{parent}' takes {len(getArgs(parent))} custom argument{sinplu(len(args))} but {len(args)} {sinplu(len(args), 'was', 'were')} given"
		argCount = f"{len(getArgs(parent))}"
		argsPrettyPrint1 = ["'"+i+"'" for i in getArgs(parent)]
		argsPrettyPrint = f"{', '.join(argsPrettyPrint1)}"
		error = f"objects of class '{parent}' take argument{sinplu(len(getArgs(parent)))}" + (f" ({argsPrettyPrint}) " if len(getArgs(parent)) >= 1 else f"no arguments ") + f"but object '{name}' is given" + ((f" '{', '.join(list(args.keys()))}'") if len(args.keys()) > 0 else " none")
		raise TypeError(error)


	if all(checks[:-4]):
		print(checks)
		#error = f"Keys: '{args.keys()}', Keys2: '{getArgs(parent)}',  Class '{parent}' takes {len(getArgs(parent))} custom argument{sinplu(len(args))} but {len(args)} {sinplu(len(args), 'was', 'were')} given"
		argCount = f"{len(getArgs(parent))}"
		argsPrettyPrint1 = ["'"+i+"'" for i in getArgs(parent)]
		argsPrettyPrint = f"{', '.join(argsPrettyPrint1)}"
		error = f"objects of class '{parent}' take" + (f" {len(list(getArgs(parent)))} argument{sinplu(len(getArgs(parent)))}" if len(getArgs(parent)) >= 1 else f"no arguments ") + f" but object '{name}' is given " + (f"{len(list(args.keys()))}" if len(args.keys()) > 0 else " none")
		raise TypeError(error)
	else:
		didYouMean = 'Did you mean \'' + (bestMatch(parent, getAllClasses()) or '') + '\'' 
		raise NameError(f"No class named '{parent}'. {didYouMean}?")


def createObjects(parent = None, names:list = [], args:list = [], namesArgs:dict = {}):
	if "allowNamesArgsOption": #TODO ?
		names = names or namesArgs.keys()
		args = args or namesArgs.values()
	if not names: raise TypeError("Objects need to have a name")
	for n,i in enumerate(names):
		createObject(i, parent, args[n])
	return [classes[parent]["objects"][i] for i in names]
def createObjectsForMultipleClasses(names:list, args:list, parents=list): 
	for i in names:
		createObject(i, parent, args[i])
	return [classes[parents[n]]["objects"][i]["name"] for n,i in enumerate(names)]

def updateObject(className, objectName:str, arg:str, newArg:str): # maybe make {oldArg: newArg}, make old arg need to be specifiable to change (in cases like password change maybe?)
	if objectName in getClass(className)["constantArgs"] and ("option" and not secretArgs) : # or "option" #TODO
		getObjects(className, objectName)[arg] = newArg
	else:
		raise SyntaxError(f"Can't update constant argument '{arg}'")
def deleteObject(className, objectName:str): del getObjects(className)[objectName]


# ----------------- callbacks
def onNewClass(callback): onNewClass = callback
def onNewObject(callback): onNewObject = callback
def onDeleteClass(callback): onDeleteClass = callback
def onDeleteObject(callback): onDeleteObject = callback
def onUpdateObject(callback): onUpdateObject = callback
def onUpdateClass(callback): onUpdateClass = callback
