from graphMachine import GraphMachine
from Utilities.constructors import *
from Utilities.pretty_representation import *


# Test Data
testData = " The wing was established in July 1950 and headquartered at Changi, on the east coast of Singapore. "

# Set up ChainGraphLayer
originalChainGraphLayer = chainGraphLayerFromString(testData)
originalChainGraphLayer.classify(loadDataClasses("letters"))

# Create DataGraphMachine and feed data
flowGraphs = loadFlowGraphs(["word", "number", "punctuation", "whiteSpace"])
graphMachine = GraphMachine(flowGraphs, originalChainGraphLayer)
graphMachine.feed_chain_graph_layer(originalChainGraphLayer)

dataClasses = loadDataClasses("words")
graphMachine.chainGraphLayer.classify(dataClasses)

print(pretty_chainGraphLayer(graphMachine.chainGraphLayer))
