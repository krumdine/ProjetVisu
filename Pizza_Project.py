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

######################
## Config

# rootPath = os.getcwd()
rootPath = "/net/cremi/vbocquel/Cours/S9_BioVisu/ProjetVisu/"
# rootPath = "/net/cremi/jturon/BioInfosEtVisu/Visu/Projet/"

def main(graph): 
	# Default Properties
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
	generateGraph(graph)
	createMessageLengthProperty(graph)
	analyzeRequestMessage(graph)
	# Display
#	updateVisualization()

	
def analyzeRequestMessage(graph):
	viewLabel = graph.getStringProperty("viewLabel")
	narratives = {
		"money":{"keywords":[],"node":None},
		"job":{"keywords":[],"node":None},
		"family":{"keywords":[],"node":None},
		"student":{"keywords":[],"node":None},
		"desire":{"keywords":[],"node":None}
	}

	basePath =  os.path.join(rootPath,"pizza_request_dataset","narratives")
	for k in narratives:
		narratives[k]["node"] = graph.addNode()
		viewLabel.setNodeStringValue(narratives[k]["node"], k)
		with open(os.path.join(basePath, k+".txt"),'r') as f:
			narratives[k]["keywords"] = f.read().split('\r\n')
	
	for n in graph.getNodes():
		request = graph.getStringProperty("request_text").getNodeValue(n)
		for k in narratives:
			cpt = 0
			for keyWord in narratives[k]["keywords"]:
				cpt += request.count(keyWord)
			if(cpt > 2):
				graph.addEdge(n,narratives[k]["node"])

# def generateSubreddits(graph):
#	gotPizza = graph.getSubGraph("gotPizza")
#	didntGotPizza = graph.getSubGraph("didntGotPizza")
#	
#	sub = graph.getStringVectorProperty("requester_subreddits_at_request")
#	
#	for n in didntGotPizza.getNodes():
#		subreddits = sub.getNodeValue(n)
#		for s in subreddits:
#			subGraph = didntGotPizza.getSubGraph(s)
#			if subGraph is None:
#				subGraph = didntGotPizza.addSubGraph(s)
#			subGraph.addNode(n)

def createMessageLengthProperty(graph):
	messageLength = graph.getIntegerProperty("messageLength")
	post = graph.getStringProperty("request_text_edit_aware")
	for n in graph.getNodes():
		messageLength.setNodeValue(n,len(post.getNodeValue(n)))

## Add nodes from the dataset
def generateGraph(graph):
	graph.setName("RAOP")
	path = os.path.join(rootPath, "pizza_request_dataset", "pizza_request_dataset.json")
	dataset = read_dataset(path)
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
	
	# Generate subsubgraph on each subgraph depending on the test set property
#	generateSubGraphTestSet(graphe, gotPizza)
#	generateSubGraphTestSet(graphe, didntGotPizza)
	
	
## Add subgraph depending on if node are in test set
def generateSubGraphTestSet(graph, subgraph):
		ITS = []
		OTS = []
		inTestSetProperty = graph.getBooleanProperty('in_test_set')
		for n in subgraph.getNodes() :
			if inTestSetProperty.getNodeValue(n):
				ITS.append(n)
			else:
				OTS.append(n)
		inTestSet = subgraph.inducedSubGraph(ITS)
		inTestSet.setName("inTestSet")
		outTestSet = subgraph.inducedSubGraph(OTS)
		outTestSet.setName("outTestSet")


## Conveniant function to retrieve data from json file
def read_dataset(path):
	with codecs.open(path, 'r', 'utf-8') as myFile:
		content = myFile.read()
	dataset = json.loads(content)
	return dataset


## Test if two requesters have at least one common subreddit
def hasSubredditInCommon(graph, m, n):
	subreddit = graph.getStringVectorProperty("requester_subreddits_at_request")
	return len(set(subreddit.getNodeValue(m)).intersection(set(subreddit.getNodeValue(n)))) > 0


def generateEdgesOnCommonSubreddit(graph):
	nodes = list(graph.getNodes())
	nbNodes = len(nodes)
	for i in range(0,nbNodes-1):
		for j in range(i+1,nbNodes):
				if hasSubredditInCommon(graph, nodes[i], nodes[j]):
					graph.addEdge(nodes[i],nodes[j])
