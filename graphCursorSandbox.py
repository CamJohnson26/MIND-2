from dataNode import DataNode
from graphNode import GraphNode
from graphStructure import GraphStructure
from dataGraph import DataGraph
from dataGraphLayer import DataGraphLayer
from dataGraphMachine import DataGraphMachine
from dataType import DataType
from Utilities.dataTypeConstructor import *
from Utilities.dataNodeConstructor import *
from Utilities.flowGraphConstructor import *
from Utilities.dataClassConstructor import *

# Setup Input Strings
testData = " cameron is the man "

# Convert string to chain of GraphNodes
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

# Create Data Graphs
wordDataGraph = loadFlowGraph("word.json")
numberDataGraph = loadFlowGraph("number.json")

# Set up DataGraph Layer
originalDataGraphLayer = DataGraphLayer(None)
originalDataGraphLayer.dataGraph = dataGraph

# Create DataGraphMachine
dataGraphMachine = DataGraphMachine([wordDataGraph, numberDataGraph], originalDataGraphLayer)

for d in dataGraph.graph.nodes:
    dataGraphMachine.feed(d)

print(dataGraphMachine.dataGraphLayer)

# Build and test a simple classifier
dataClasses = []
dataClasses.append(loadDataClass("class_a.json"))
dataClasses.append(loadDataClass("class_b.json"))

letterDataType = loadDataType("letter.json")

testA = DataNode(letterDataType, parsedData='a')
testAGraphNode = GraphNode(testA)

testA.classify(dataClasses)
print(testA)
