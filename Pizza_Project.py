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

	path = '/net/cremi/jturon/BioInfosEtVisu/Visu/Projet/pizza_request_dataset/pizza_request_dataset.json'
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

	gotPizza = graph.addSubGraph("gotPizza")
	didntGotPizza = graph.addSubGraph("didntGotPizza")
	gotPizzaProperty = graph.getBooleanProperty('requester_received_pizza')
	for n in graph.getNodes():
		if gotPizzaProperty.getNodeValue(n):
			gotPizza.addNode(n)
		else:
			didntGotPizza.addNode(n)
			
	inTestSet = gotPizza.addSubGraph('in test set')
	outTestSet = gotPizza.addSubGraph('out of test set')
	inTestSetProperty = graph.getBooleanProperty('in_test_set')
	for n in gotPizza.getNodes() :
		if inTestSetProperty.getNodeValue(n):
			inTestSet.addNode(n)
		else:
			outTestSet.addNode(n)
						
	inTestSet = didntGotPizza.addSubGraph('in test set')
	outTestSet = didntGotPizza.addSubGraph('out of test set')
	for n in didntGotPizza.getNodes() :
		if inTestSetProperty.getNodeValue(n):
			inTestSet.addNode(n)
		else:
			outTestSet.addNode(n)

	cpt = 0
	nbNode = graph.numberOfNodes()
	for n in graph.getNodes() :
		cpt = cpt + 1
		print '{} / {}'.format(cpt, nbNode)
		for m in graph.getNodes() :
			if not m == n and not graph.hasEdge(m,n):
				if hasSubredditInCommon(graph, m, n):
					graph.addEdge(m,n)

def read_dataset(path):
	with codecs.open(path, 'r', 'utf-8') as myFile:
		content = myFile.read()
	dataset = json.loads(content)
	return dataset
	
def hasSubredditInCommon(graph, m, n):
	subreddit = graph.getStringVectorProperty("requester_subreddits_at_request")
	if not len(set(subreddit.getNodeValue(m)) - set(subreddit.getNodeValue(n))) == 0 :
		return True
	return False
