from dataNode import DataNode
from graphNode import GraphNode
from graphStructure import GraphStructure
from flowGraph import FlowGraph
from dataGraph import DataGraph
from graphCursor import GraphCursor
from dataGraphLayer import DataGraphLayer
from dataGraphMachine import DataGraphMachine
from flowGraphCursor import FlowGraphCursor
from dataType import DataType
from dataClass import DataClass

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
testData = " cameron is the man "

testDataGraphNodes = []
previousNode = None
for c in testData:
    cDataType = DataType("char", lambda i: i == c)
    cDataNode = DataNode(cDataType, parsedData=c)
    cGraphNode = GraphNode(cDataNode)
    testDataGraphNodes.append(cGraphNode)
    if previousNode:
        previousNode.nexts.append(cGraphNode)
    previousNode = cGraphNode
testDataGraphNodes[-1].nexts.append(None)

testDataGraph = GraphStructure(testDataGraphNodes, "character_stream")
dataGraph = DataGraph(testDataGraph)

letterDataType = DataType("letter", letterMatch)
numberDataType = DataType("number", numberMatch)
whiteSpaceDataType = DataType("whiteSpace", whiteSpaceMatch)
punctuationDataType = DataType("punctuation", punctuationMatch)

letterNode = DataNode(letterDataType)
numberNode = DataNode(numberDataType)
whiteSpaceNode = DataNode(whiteSpaceDataType)
punctuationNode = DataNode(punctuationDataType)

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
wordDataGraph = FlowGraph(wordGraphStructure, [spaceGraphNode1])

numberGraphStructure = GraphStructure([numberGraphNode],"number")
numberDataGraph = FlowGraph(numberGraphStructure, [numberGraphNode])

originalDataGraphLayer = DataGraphLayer(None)
originalDataGraphLayer.dataGraph = dataGraph

dataGraphMachine = DataGraphMachine([wordDataGraph, numberDataGraph], originalDataGraphLayer)

for d in dataGraph.graph.nodes:
    dataGraphMachine.feed(d)

#print(dataGraphMachine.dataGraphLayer)

charDataNodeA = DataNode(letterDataType, parsedData='a')
charGraphNodeA = GraphNode(charDataNodeA)
charDataNodeA2 = DataNode(letterDataType, parsedData='A')
charGraphNodeA2 = GraphNode(charDataNodeA2)
charGraphNodeA.nexts = [None]
charGraphNodeA2.nexts = [None]
charGraphStructureA = GraphStructure([charGraphNodeA, charGraphNodeA2], "class:a")
charFlowGraphA = FlowGraph(charGraphStructureA, [charGraphNodeA, charGraphNodeA2])
dataClassA = DataClass(charFlowGraphA, 0, 'a')

charDataNodeB = DataNode(letterDataType, parsedData='b')
charGraphNodeB = GraphNode(charDataNodeB)
charDataNodeB2 = DataNode(letterDataType, parsedData='B')
charGraphNodeB2 = GraphNode(charDataNodeB2)
charGraphNodeB.nexts = [None]
charGraphNodeB2.nexts = [None]
charGraphStructureB = GraphStructure([charGraphNodeB, charGraphNodeB2], "class:b")
charFlowGraphB = FlowGraph(charGraphStructureB, [charGraphNodeB, charGraphNodeB2])
dataClassB = DataClass(charFlowGraphB, 1, 'b')

# Can we replace the matches function with comparing to the list of classes?
letterDataType = DataType("letter", letterMatch)
letterDataType.dataClasses.append(dataClassA)
letterDataType.dataClasses.append(dataClassB)

testA = DataNode(letterDataType, parsedData='A')
testAGraphNode = GraphNode(testA)

#for a in letterDataType.dataClasses:
    #print a
#print(dataClassB.matches(testA))

testA.classify()
print(testA)
print(letterGraphNode)
print(letterGraphNode.matches(GraphNode(testA)))
print(charGraphNodeA2.matches(GraphNode(testA)))
