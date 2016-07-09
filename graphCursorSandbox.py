from chainGraphLayer import ChainGraphLayer
from graphMachine import GraphMachine
from Utilities.constructors import *

# Test Data
testData = " CAMERON is , the MAN "

dataClasses = ["letters/class_a.json",
               "letters/class_b.json",
               "letters/class_c.json",
               "letters/class_d.json",
               "letters/class_e.json",
               "letters/class_f.json",
               "letters/class_g.json",
               "letters/class_h.json",
               "letters/class_i.json",
               "letters/class_j.json",
               "letters/class_k.json",
               "letters/class_l.json",
               "letters/class_m.json",
               "letters/class_n.json",
               "letters/class_o.json",
               "letters/class_p.json",
               "letters/class_q.json",
               "letters/class_r.json",
               "letters/class_s.json",
               "letters/class_t.json",
               "letters/class_u.json",
               "letters/class_v.json",
               "letters/class_w.json",
               "letters/class_x.json",
               "letters/class_y.json",
               "letters/class_y.json"]

# Set up ChainGraphLayer
originalChainGraphLayer = ChainGraphLayer(None)
originalChainGraphLayer.chainGraph = chainGraphFromString(testData)
originalChainGraphLayer.classify(loadDataClasses(dataClasses))
# Create DataGraphMachine and feed data
flowGraphs = [loadFlowGraph("word.json"), loadFlowGraph("number.json"), loadFlowGraph("punctuation.json"), loadFlowGraph("whiteSpace.json")]
graphMachine = GraphMachine(flowGraphs, originalChainGraphLayer)
graphMachine.feed_chain_graph_layer(originalChainGraphLayer)
graphMachine.chainGraphLayer.classify([loadDataClass("words/cameron.json"), loadDataClass("words/is.json"), loadDataClass("words/the.json")])
print(graphMachine.chainGraphLayer)
