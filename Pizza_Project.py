# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import *
import codecs
import json

# the updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# the pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# the main(graph) function must be defined 
# to run the script on the current graph

########################
### Global variables ###
########################
category = ["family","job","student","money","desire"]

# rootPath = os.getcwd()
# rootPath = "/net/cremi/vbocquel/Cours/S9_BioVisu/ProjetVisu/"
 rootPath = "/net/cremi/jturon/BioInfosEtVisu/Visu/Projet/"


def main(graph): 
	viewBorderColor = graph.getColorProperty("viewBorderColor")
	viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
	viewColor = graph.getColorProperty("viewColor")
	viewFont = graph.getStringProperty("viewFont")
	viewFontSize = graph.getIntegerProperty("viewFontSize")
	viewLabel = graph.getStringProperty("viewLabel")
	viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
	viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
	viewLabelColor = graph.getColorProperty("viewLabelColor")
	viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
	viewLayout = graph.getLayoutProperty("viewLayout")
	viewMetric = graph.getDoubleProperty("viewMetric")
	viewRotation = graph.getDoubleProperty("viewRotation")
	viewSelection = graph.getBooleanProperty("viewSelection")
	viewShape = graph.getIntegerProperty("viewShape")
	viewSize = graph.getSizeProperty("viewSize")
	viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
	viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
	viewTexture = graph.getStringProperty("viewTexture")
	viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
	viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")
	# Preprocess data
#	generateGraph(graph)
#	colorNodes(graph)
#	categorizeNodes(graph,3)
#	subGraphsPerCategory(graph)
#	stats(graph)

########################

def subGraphsPerCategory(graph):		
	subGraphs = { "family" : [],"job" : [],"student" : [],"money" : [],"desire" : []}	
		
	for n in graph.getNodes():
		if(not viewLabel.getNodeValue(n) in ["family","job","student","money","desire"]):
			for m in graph.getInOutNodes(n):
				subGraphs[viewLabel.getNodeValue(m)].append(n)
		else:
			for i in category:
				subGraphs[i].append(n)
	for i in subGraphs.keys():
		graph.inducedSubGraph(subGraphs[i]).setName(i)

def stats(graph):
	received = graph.getBooleanProperty("requester_received_pizza")
	viewLabel = graph.getStringProperty("viewLabel")
	
	for n in graph.getNodes():
		if( viewLabel.getNodeValue(n) in ["family","job","student","money","desire"]):
			cpt = 0.
			cptMax = 0.
			for m in graph.getInOutNodes(n):
				cptMax += 1.
				if( received.getNodeValue(m) ):
					cpt += 1.
			print viewLabel.getNodeValue(n) + " : " + str(cpt) + "/" + str(cptMax) + "=>" + str((cpt/cptMax)*100.)
	
	print '\n'
	
	res = [[0.,0.],[0.,0.], [0.,0.], [0.,0.], [0.,0.], [0.,0.]]
	
	res4 = { "family" : 0,"job" : 0,"student" : 0,"money" : 0,"desire" : 0}
	res5 = { "family" : 0,"job" : 0,"student" : 0,"money" : 0,"desire" : 0}
	
	for n in graph.getNodes():
		if( not viewLabel.getNodeValue(n) in ["family","job","student","money","desire"]):
			cpt = 0
			for m in graph.getInOutNodes(n):
				cpt += 1
			res[cpt][1] += 1.
			if( received.getNodeValue(n) ):
				res[cpt][0] += 1.
			if(cpt == 4):
				for m in graph.getInOutNodes(n):
					res4[viewLabel.getNodeValue(m)]+=1
			if(cpt == 5):
				for m in graph.getInOutNodes(n):
					res5[viewLabel.getNodeValue(m)]+=1

	for i in range(0,6):
		print str(res[i][0]) + '/' + str(res[i][1]) + ' => ' + str( 100. * (res[i][0]/ res[i][1]))
	
	print '\n'	
	
	print res4
	print res5

def categorizeNodes(graph, s):
	viewLabel = graph.getStringProperty("viewLabel")
	basePath = os.path.join(rootPath, 'pizza_request_dataset', 'narratives')

	narratives = {"money":{"keywords","node"},"job":{"keywords","node"},"family":{"keywords","node"},"student":{"keywords","node"},"desire":{"keywords","node"}}

	for k in narratives:
		narratives[k]["node"] = graph.addNode()
		viewLabel.setNodeStringValue(narratives[k]["node"], k)
		with open(basePath+k+'.txt','r') as f:
			narratives[k]["keywords"] = f.read().split('\r\n')
	
	for n in graph.getNodes():
		request = graph.getStringProperty("request_text").getNodeValue(n)
		for k in narratives:
			cpt = 0
			for keyWord in narratives[k]["keywords"]:
				cpt += request.count(keyWord)
			if(cpt > s):
				graph.addEdge(n,narratives[k]["node"])

def colorNodes(graph):
	gotPizza = graph.getSubGraph("gotPizza")
	didntGotPizza = graph.getSubGraph("didntGotPizza")
	viewColor = graph.getColorProperty("viewColor")
	for n in gotPizza.getNodes():
		viewColor.setNodeValue(n,tlp.Color(0,255,0,255))
	for n in didntGotPizza.getNodes():
		viewColor.setNodeValue(n,tlp.Color(0,0,255,255))

def generateGraph(graph):
	graph.setName("RAOP")	
	path = os.path.join('pizza_request_dataset','pizza_request_dataset.json')
	dataset = read_dataset(path)

	# Build graph and add properties
	for r in dataset:
		newNode = graph.addNode()
		for key in dataset[0].keys():
			valueType = type(dataset[0][key])
			if valueType is int:
				graph.getIntegerProperty(key).setNodeValue(newNode,r[key])
			elif valueType is unicode:
				text = "" if r[key] is None else r[key]
				graph.getStringProperty(key).setNodeValue(newNode,text)
			elif valueType is float:
				graph.getDoubleProperty(key).setNodeValue(newNode,r[key])
			elif valueType is bool:
				graph.getBooleanProperty(key).setNodeValue(newNode,r[key])
			elif valueType is list:
				graph.getStringVectorProperty(key).setNodeValue(newNode,r[key])

	# Generate subgraphes depending on the success of the request
	GP = []
	DGP = []
	gotPizzaProperty = graph.getBooleanProperty('requester_received_pizza')
	for n in graph.getNodes():
		if gotPizzaProperty.getNodeValue(n):
			GP.append(n)
		else:
			DGP.append(n)
	gotPizza = graph.inducedSubGraph(GP)
	gotPizza.setName("gotPizza")	
	didntGotPizza = graph.inducedSubGraph(DGP)
	didntGotPizza.setName("didntGotPizza")

def read_dataset(path):
	with codecs.open(path, 'r', 'utf-8') as myFile:
		content = myFile.read()
	dataset = json.loads(content)
	return dataset
	
def hasSubredditInCommon(graph, m, n):
	subreddit = graph.getStringVectorProperty("requester_subreddits_at_request")
	intersection = set(subreddit.getNodeValue(m)).intersection(set(subreddit.getNodeValue(n)))
	return len(intersection) > 0

def messageLength(graph):
	messageLength = graph.getIntegerProperty("messageLength")
	post = graph.getStringProperty("request_text_edit_aware")
	
	for n in graph.getNodes():
		messageLength.setNodeValue(n,len(post.getNodeValue(n)))
