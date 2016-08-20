from graphMachine import GraphMachine
from Utilities.constructors import *
from Utilities.pretty_representation import *

dtfm = DataTypeFileManager()
dnfm = DataNodeFileManager()
dcfm = DataClassFileManager()
fgfm = FlowGraphFileManager()

# Test Data

# testData = " The wing was established in July 1950 and headquartered at Changi, on the east coast of Singapore. "
# testData = " Headquartered in the east coast, Singapore become Changi in July 1950"
# testData = " El burro de coolest Ross barfed happily nor sadly "
testData = " The 1998 FA Charity Shield was the 76th in a series of annual English football matches organised by The Football Association and usually played between the winners of the previous season's Premier League and FA Cup competitions. It was contested on 9 August 1998 by Arsenal, who won both titles the previous season, and Manchester United, the league runners-up. Watched by a crowd of 67,342 at Wembley Stadium (pictured), United began the game strongly, but Arsenal took the lead when Marc Overmars scored 11 minutes before half-time. They extended their lead in the second half, as Overmars and Nicolas Anelka found Christopher Wreh, who put the ball into an empty net at the second attempt. In the 72nd minute, Arsenal scored a third goal, when Anelka got around Jaap Stam in the penalty box and shot the ball past goalkeeper Peter Schmeichel. Arsenal won the match 30, United's first defeat in the Shield in 13 years. United completed a treble of trophies in the 199899 season, winning the league, the FA Cup and the UEFA Champions League. "
#testData = " aaron act "

# Set up ChainGraphLayer
originalChainGraphLayer = chainGraphLayerFromString(testData)
originalChainGraphLayer.classify([dtfm.loadObject("letter.json")])
# print(originalChainGraphLayer)
# print(pretty_chainGraphLayer(originalChainGraphLayer))

# Create DataGraphMachine and feed data
flowGraphs = fgfm.loadObjects(["word", "number", "punctuation", "whiteSpace"])
graphMachine = GraphMachine(flowGraphs, originalChainGraphLayer)
graphMachine.feed_chain_graph_layer(originalChainGraphLayer)

# print(graphMachine.chainGraphLayer)
graphMachine.chainGraphLayer.classify([dtfm.loadObject("word.json")])

# print(graphMachine.chainGraphLayer)
print(pretty_chainGraphLayer(graphMachine.chainGraphLayer))
