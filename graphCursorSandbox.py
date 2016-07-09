from graphMachine import GraphMachine
from Utilities.constructors import *

# Test Data
testData = " CAMERON is , the MAN "

# Set up ChainGraphLayer
originalChainGraphLayer = chainGraphLayerFromString(testData)
originalChainGraphLayer.classify(loadDataClasses("letters"))

# Create DataGraphMachine and feed data
flowGraphs = loadFlowGraphs(["word", "number", "punctuation", "whiteSpace"])
graphMachine = GraphMachine(flowGraphs, originalChainGraphLayer)
graphMachine.feed_chain_graph_layer(originalChainGraphLayer)

dataClasses = loadDataClasses("words")
graphMachine.chainGraphLayer.classify(dataClasses)

print(graphMachine.chainGraphLayer)
