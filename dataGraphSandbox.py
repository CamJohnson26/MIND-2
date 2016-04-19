from dataNode import DataNode
from graphNode import GraphNode
from graphStructure import GraphStructure
from dataGraph import DataGraph
from dataGraphFlattener import DataGraphFlattener
from parseNode import ParseNode
from dataGraphLayer import DataGraphLayer

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

testData = " this is to test "
testDataGraphNodes = []
previousNode = None
for c in testData:
    cDataNode = DataNode("char", lambda i: i == c, parsedData=c)
    cGraphNode = GraphNode(cDataNode)
    testDataGraphNodes.append(cGraphNode)
    if previousNode:
        previousNode.nexts.append(cGraphNode)
    previousNode = cGraphNode
testDataGraphNodes[-1].nexts.append(None)
testDataGraph = GraphStructure(testDataGraphNodes, "character_stream")
dataGraph = DataGraph(testDataGraph)


test2Data = ["this", "is", "to", "test"]
test2DataGraphNodes = []
previousNode = None
for c in test2Data:
    cDataNode = DataNode("word", lambda i: i == c, parsedData=c)
    cGraphNode = GraphNode(cDataNode)
    test2DataGraphNodes.append(cGraphNode)
    if previousNode:
        previousNode.nexts.append(cGraphNode)
    previousNode = cGraphNode
test2DataGraphNodes[-1].nexts.append(None)
test2DataGraph = GraphStructure(test2DataGraphNodes, "word_stream")
data2Graph = DataGraph(test2DataGraph)


testNode = GraphNode(DataNode("abc",lambda a:a, ""))
testNode.nexts = [None]
dataGraph.graph.nodes.append(testNode)
dataGraph.graph.nodes[0].nexts.append(testNode)

dataGraphFlattener = DataGraphFlattener(dataGraph)
flatGraph = dataGraphFlattener.flat_graph()

parseNode1 = ParseNode()
parseNode1.startGraphNode = testDataGraph.nodes[0]
parseNode1.endGraphNode = testDataGraph.nodes[5]
parseNode1.targetGraphNode = test2DataGraph.nodes[0]
parseNode2 = ParseNode()
parseNode2.startGraphNode = testDataGraph.nodes[5]
parseNode2.endGraphNode = testDataGraph.nodes[8]
parseNode2.targetGraphNode = test2DataGraph.nodes[1]
parseNode3 = ParseNode()
parseNode3.startGraphNode = testDataGraph.nodes[8]
parseNode3.endGraphNode = testDataGraph.nodes[11]
parseNode3.targetGraphNode = test2DataGraph.nodes[2]
parseNode4 = ParseNode()
parseNode4.startGraphNode = testDataGraph.nodes[11]
parseNode4.endGraphNode = testDataGraph.nodes[16]
parseNode4.targetGraphNode = test2DataGraph.nodes[3]

parseNodes = [parseNode1, parseNode2, parseNode3, parseNode4]

#print(dataGraph)
#for n in parseNodes:
#    print(n)

dataGraphLayer = DataGraphLayer(dataGraph, data2Graph, parseNodes)

print(dataGraphLayer)
