from dataNode import DataNode
from graphNode import GraphNode
from graphStructure import GraphStructure
from flowGraph import FlowGraph
from dataGraph import DataGraph
from graphCursor import GraphCursor
from dataGraphLayer import DataGraphLayer
from dataGraphMachine import DataGraphMachine
from flowGraphCursor import FlowGraphCursor

def letterMatch(test):
    returnVal = False
    if type(test) is str and test in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
        returnVal = True
    return returnVal


def numberMatch(test):
    returnVal = False
    if type(test) is str and test in ['1','2','3','4','5','6','7','8','9','0']:
        returnVal = True
    return returnVal


def whiteSpaceMatch(test):
    returnVal = False
    if type(test) is str and test in ['\t',' ','\n']:
        returnVal = True
    return returnVal


def punctuationMatch(test):
    returnVal = False
    if type(test) is str and test in ['!','@','#','$','%','^','&','*','(',')',',','.','?','\'','\"']:
        returnVal = True
    return returnVal

testData = " this is to test word tokenizer 2 and see if I recieve 1999 reliable informations "
testData = " forescore and 7 years ago our forefathers brought forth on this continent-a new nation"

testDataGraphNodes = []
previousNode = None
for c in testData:
    cDataNode = DataNode("char", lambda i: i == c, parsedData=c)
    cGraphNode = GraphNode(cDataNode)
    testDataGraphNodes.append(cGraphNode)
    if previousNode:
        previousNode.nexts.append(cGraphNode)
    previousNode = cGraphNode
testDataGraphNodes[-1].nexts.append(None)

testDataGraph = GraphStructure(testDataGraphNodes, "character_stream")
dataGraph = DataGraph(testDataGraph)


letterNode = DataNode("letter", letterMatch)
numberNode = DataNode("number", numberMatch)
whiteSpaceNode = DataNode("whiteSpace", whiteSpaceMatch)
punctuationNode = DataNode("punctuation", punctuationMatch)

spaceGraphNode1 = GraphNode(whiteSpaceNode)
letterGraphNode = GraphNode(letterNode)
spaceGraphNode2 = GraphNode(whiteSpaceNode)
numberGraphNode = GraphNode(numberNode)

spaceGraphNode1.nexts.append(letterGraphNode)
letterGraphNode.nexts.append(spaceGraphNode2)
letterGraphNode.nexts.append(letterGraphNode)
spaceGraphNode2.nexts.append(None)
numberGraphNode.nexts.append(numberGraphNode)
numberGraphNode.nexts.append(None)

wordGraphStructure = GraphStructure([spaceGraphNode1, letterGraphNode, spaceGraphNode2], "word")
wordDataGraph = FlowGraph(wordGraphStructure)

numberGraphStructure = GraphStructure([numberGraphNode],"number")
numberDataGraph = FlowGraph(numberGraphStructure)

originalDataGraphLayer = DataGraphLayer(None)
originalDataGraphLayer.dataGraph = dataGraph

dataGraphMachine = DataGraphMachine([wordDataGraph, numberDataGraph], originalDataGraphLayer)

for d in dataGraph.graph.nodes:
    dataGraphMachine.feed(d)

print(dataGraphMachine.dataGraphLayer)
