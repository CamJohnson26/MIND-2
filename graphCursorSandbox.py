from graphMachine import GraphMachine
from Utilities.constructors import *
from Utilities.pretty_representation import *


# Test Data
#testData = " The wing was established in July 1950 and headquartered at Changi, on the east coast of Singapore. "
testData = " Headquartered in the east coast, Singapore established Changi in July 1950"

# Set up ChainGraphLayer
originalChainGraphLayer = chainGraphLayerFromString(testData)
originalChainGraphLayer.classify({"letter": loadDataClasses("letters")})

# Create DataGraphMachine and feed data
flowGraphs = loadFlowGraphs(["word", "number", "punctuation", "whiteSpace"])
graphMachine = GraphMachine(flowGraphs, originalChainGraphLayer)
graphMachine.feed_chain_graph_layer(originalChainGraphLayer)


dataClasses = {}
dataClasses["word"] = loadDataClasses("words")
graphMachine.chainGraphLayer.classify(dataClasses)
pretty_chainGraphLayer(graphMachine.chainGraphLayer)

# Tokenize by part of speech
flowGraphs = loadFlowGraphs(["words/articles/article", "words/prepositions/preposition", "words/properNouns/properNoun","words/verbs/verb","words/nouns/noun","words/adjectives/adjective","words/conjunctions/conjunction","punctuation","whiteSpace","number"])
graphMachine.flowGraphs = flowGraphs
graphMachine.feed_chain_graph_layer(graphMachine.chainGraphLayer)

dataClasses["article"] = loadDataClasses("words/articles")
dataClasses["noun"] = loadDataClasses("words/nouns")
dataClasses["properNoun"] = loadDataClasses("words/properNouns")
dataClasses["verb"] = loadDataClasses("words/verbs")
dataClasses["adjective"] = loadDataClasses("words/adjectives")
dataClasses["conjunction"] = loadDataClasses("words/conjunctions")
dataClasses["preposition"] = loadDataClasses("words/prepositions")

graphMachine.chainGraphLayer.classify(dataClasses)
print(pretty_chainGraphLayer(graphMachine.chainGraphLayer))
