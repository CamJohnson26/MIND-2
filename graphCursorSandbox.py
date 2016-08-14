from graphMachine import GraphMachine
from Utilities.constructors import *
from Utilities.pretty_representation import *


# Test Data
#testData = " The wing was established in July 1950 and headquartered at Changi, on the east coast of Singapore. "
testData = " Headquartered in the east coast, Singapore established Changi in July 1950"
#testData = " El burro de coolest Ross barfed happily nor sadly "
#testData = " The 1998 FA Charity Shield was the 76th in a series of annual English football matches organised by The Football Association and usually played between the winners of the previous season's Premier League and FA Cup competitions. It was contested on 9 August 1998 by Arsenal, who won both titles the previous season, and Manchester United, the league runners-up. Watched by a crowd of 67,342 at Wembley Stadium (pictured), United began the game strongly, but Arsenal took the lead when Marc Overmars scored 11 minutes before half-time. They extended their lead in the second half, as Overmars and Nicolas Anelka found Christopher Wreh, who put the ball into an empty net at the second attempt. In the 72nd minute, Arsenal scored a third goal, when Anelka got around Jaap Stam in the penalty box and shot the ball past goalkeeper Peter Schmeichel. Arsenal won the match 30, United's first defeat in the Shield in 13 years. United completed a treble of trophies in the 199899 season, winning the league, the FA Cup and the UEFA Champions League. "

# Set up ChainGraphLayer
originalChainGraphLayer = chainGraphLayerFromString(testData)
originalChainGraphLayer.classify([loadDataType("letter.json")])
print(pretty_chainGraphLayer(originalChainGraphLayer))

# Create DataGraphMachine and feed data
flowGraphs = loadFlowGraphs(["word", "number", "punctuation", "whiteSpace"])
graphMachine = GraphMachine(flowGraphs, originalChainGraphLayer)
graphMachine.feed_chain_graph_layer(originalChainGraphLayer)

graphMachine.chainGraphLayer.classify([loadDataType("word.json")])
print(pretty_chainGraphLayer(graphMachine.chainGraphLayer))

# Tokenize by part of speech
flowGraphs = loadFlowGraphs(["words/adverbs/adverb","words/articles/article", "words/prepositions/preposition", "words/properNouns/properNoun","words/verbs/verb","words/nouns/noun","words/adjectives/adjective","words/conjunctions/conjunction","punctuation","whiteSpace","number"])
graphMachine.flowGraphs = flowGraphs
graphMachine.feed_chain_graph_layer(graphMachine.chainGraphLayer)

dataTypes = ["adverb", "article", "noun", "properNoun", "verb", "adjective", "conjunction", "preposition"]

graphMachine.chainGraphLayer.classify(loadDataTypes(dataTypes))
print(pretty_chainGraphLayer(graphMachine.chainGraphLayer))
