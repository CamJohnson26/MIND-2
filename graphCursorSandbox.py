from dataNode import DataNode
from graphNode import GraphNode
from chainGraphLayer import ChainGraphLayer
from graphMachine import GraphMachine
from Utilities.dataTypeConstructor import *
from Utilities.dataNodeConstructor import *
from Utilities.flowGraphConstructor import *
from Utilities.dataClassConstructor import *
from Utilities.chainGraphConstructor import *

testData = " cameron is the man "
chainGraph = chainGraphFromString(testData)

# Create Data Graphs
wordFlowGraph = loadFlowGraph("word.json")
numberFlowGraph = loadFlowGraph("number.json")

# Set up DataGraph Layer
originalChainGraphLayer = ChainGraphLayer(None)
originalChainGraphLayer.chainGraph = chainGraph

# Create DataGraphMachine
graphMachine = GraphMachine([wordFlowGraph, numberFlowGraph], originalChainGraphLayer)

for d in chainGraph.graph.nodes:
    graphMachine.feed(d)

print(graphMachine.chainGraphLayer)

# Build and test a simple classifier
dataClasses = []
dataClasses.append(loadDataClass("class_a.json"))
dataClasses.append(loadDataClass("class_b.json"))

letterDataType = loadDataType("letter.json")

testA = DataNode(letterDataType, parsedData='a')
testAGraphNode = GraphNode(testA)

testA.classify(dataClasses)
print(testA)
