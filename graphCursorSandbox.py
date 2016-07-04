from chainGraphLayer import ChainGraphLayer
from graphMachine import GraphMachine
from Utilities.constructors import *

# Test Data
testData = " cameron is the man "

# Set up ChainGraphLayer
originalChainGraphLayer = ChainGraphLayer(None)
originalChainGraphLayer.chainGraph = chainGraphFromString(testData)

# Create DataGraphMachine and feed data
flowGraphs = [loadFlowGraph("word.json"), loadFlowGraph("number.json")]
graphMachine = GraphMachine(flowGraphs, originalChainGraphLayer)
graphMachine.feedChainGraphLayer(originalChainGraphLayer)

print(graphMachine.chainGraphLayer)

# Build and test a simple classifier
dataClasses = []
dataClasses.append(loadDataClass("class_a.json"))
dataClasses.append(loadDataClass("class_b.json"))

letterDataType = loadDataType("letter.json")

testA = loadDataNode("char_a.json")

testA.classify(dataClasses)
print(testA)
