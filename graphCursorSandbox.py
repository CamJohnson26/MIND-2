from dataNode import DataNode
from graphNode import GraphNode
from graphStructure import GraphStructure
from flowGraph import FlowGraph
from dataGraph import DataGraph
from dataGraphLayer import DataGraphLayer
from dataGraphMachine import DataGraphMachine
from dataType import DataType
from dataClass import DataClass
import Data.matchFunctions as mf

testData = " this is to test word tokenizer 2 and see if I recieve 1999 reliable informations "
testData = " cameron is the man "

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

letterDataType = DataType("letter", mf.letterMatch)
numberDataType = DataType("number", mf.numberMatch)
whiteSpaceDataType = DataType("whiteSpace", mf.whiteSpaceMatch)
punctuationDataType = DataType("punctuation", mf.punctuationMatch)

letterNode = DataNode(letterDataType)
numberNode = DataNode(numberDataType)
whiteSpaceNode = DataNode(whiteSpaceDataType)
punctuationNode = DataNode(punctuationDataType)

spaceGraphNode1 = GraphNode(whiteSpaceNode)
letterGraphNode = GraphNode(letterNode)
spaceGraphNode2 = GraphNode(whiteSpaceNode)
numberGraphNode = GraphNode(numberNode)

spaceGraphNode1.nexts.append(letterGraphNode)
letterGraphNode.nexts.append(spaceGraphNode2)
letterGraphNode.nexts.append(letterGraphNode)
spaceGraphNode2.nexts.append(None)
numberGraphNode.nexts.append(numberGraphNode)
numberGraphNode.nexts.append(None)

wordGraphStructure = GraphStructure([spaceGraphNode1, letterGraphNode, spaceGraphNode2], "word")
wordDataGraph = FlowGraph(wordGraphStructure, [spaceGraphNode1])

print(wordDataGraph)

numberGraphStructure = GraphStructure([numberGraphNode],"number")
numberDataGraph = FlowGraph(numberGraphStructure, [numberGraphNode])

originalDataGraphLayer = DataGraphLayer(None)
originalDataGraphLayer.dataGraph = dataGraph

dataGraphMachine = DataGraphMachine([wordDataGraph, numberDataGraph], originalDataGraphLayer)

for d in dataGraph.graph.nodes:
    dataGraphMachine.feed(d)

print(dataGraphMachine.dataGraphLayer)

charDataNodeA = DataNode(letterDataType, parsedData='a')
charGraphNodeA = GraphNode(charDataNodeA)
charDataNodeA2 = DataNode(letterDataType, parsedData='A')
charGraphNodeA2 = GraphNode(charDataNodeA2)
charGraphNodeA.nexts = [None]
charGraphNodeA2.nexts = [None]
charGraphStructureA = GraphStructure([charGraphNodeA, charGraphNodeA2], "class:a")
charFlowGraphA = FlowGraph(charGraphStructureA, [charGraphNodeA, charGraphNodeA2])
dataClassA = DataClass(charFlowGraphA, 0, 'a')

charDataNodeB = DataNode(letterDataType, parsedData='b')
charGraphNodeB = GraphNode(charDataNodeB)
charDataNodeB2 = DataNode(letterDataType, parsedData='B')
charGraphNodeB2 = GraphNode(charDataNodeB2)
charGraphNodeB.nexts = [None]
charGraphNodeB2.nexts = [None]
charGraphStructureB = GraphStructure([charGraphNodeB, charGraphNodeB2], "class:b")
charFlowGraphB = FlowGraph(charGraphStructureB, [charGraphNodeB, charGraphNodeB2])
dataClassB = DataClass(charFlowGraphB, 1, 'b')

# Can we replace the matches function with comparing to the list of classes?
letterDataType = DataType("letter", mf.letterMatch)
letterDataType.dataClasses.append(dataClassA)
letterDataType.dataClasses.append(dataClassB)

testA = DataNode(letterDataType, parsedData='A')
testAGraphNode = GraphNode(testA)

#for a in letterDataType.dataClasses:
    #print a
#print(dataClassB.matches(testA))

testA.classify()
print(testA)
print(letterGraphNode)
print(letterGraphNode.matches(GraphNode(testA)))
print(charGraphNodeA2.matches(GraphNode(testA)))

from Utilities.dataClassConstructor import dataClassFromJSON
from Utilities.dataTypeConstructor import dataTypeFromJSON
from Utilities.dataNodeConstructor import dataNodeFromJSON
from Utilities.graphNodeConstructor import graphNodeFromJSON
from Utilities.graphStructureConstructor import graphStructureFromJSON
from Utilities.flowGraphConstructor import flowGraphFromJSON

newWhiteSpace = dataTypeFromJSON('''{
                        "class": "DataType", 
                        "dataTypeName": "whiteSpace",
                        "matchFunction": "whiteSpaceMatch",
                        "dataClasses":[]
                    }''')

genDataNode = dataNodeFromJSON('''{
    "dataType": {
        "matchFunction": "letterMatch", 
        "dataClasses": [], 
        "class": "DataType", 
        "dataTypeName": "letter"
    }, 
    "parsedData": "A", 
    "class": "DataNode", 
    "dataClass": {
        "dataClassIndex": 0, 
        "dataClassString": "a", 
        "class": "DataClass", 
        "flowGraph": {
            "graph": {
                "nodes": [
                    {
                        "guid": "cbe811f2-332f-48f2-9485-c8d8086dc087", 
                        "dataNode": {
                            "dataType": {
                                "matchFunction": "letterMatch", 
                                "dataClasses": [], 
                                "class": "DataType", 
                                "dataTypeName": "letter"
                            }, 
                            "parsedData": "a", 
                            "class": "DataNode", 
                            "dataClass": null
                        }, 
                        "class": "GraphNode", 
                        "nexts": [
                            null
                        ]
                    }, 
                    {
                        "guid": "2ca33464-cea7-4317-b78d-5dce5abce965", 
                        "dataNode": {
                            "dataType": {
                                "matchFunction": "letterMatch", 
                                "dataClasses": [], 
                                "class": "DataType", 
                                "dataTypeName": "letter"
                            }, 
                            "parsedData": "A", 
                            "class": "DataNode", 
                            "dataClass": null
                        }, 
                        "class": "GraphNode", 
                        "nexts": [
                            null
                        ]
                    }
                ], 
                "guid": "59282a89-f60a-4e81-83ef-101e428ae7ee", 
                "class": "GraphStructure", 
                "name": "class:a"
            }, 
            "class": "FlowGraph", 
            "startNodes": [
                "cbe811f2-332f-48f2-9485-c8d8086dc087", 
                "2ca33464-cea7-4317-b78d-5dce5abce965"
            ]
        }
    }
}''')

genGraphNode = graphNodeFromJSON('''{
                        "guid": "21169d37-90de-453c-86d7-c1d433f8301b", 
                        "dataNode": {
                            "dataType": {
                                "class": "DataType",
                                "dataTypeName": "whiteSpace",
                                "matchFunction": "whiteSpaceMatch",
                                "dataClasses":[]
                            },
                            "parsedData": null,
                            "class": "DataNode",
                            "dataClass": null
                        }, 
                        "class": "GraphNode", 
                        "nexts": [
                            "c8c292cc-e81f-4e36-8498-7660e5931e8d"
                        ]
                    }''')

genGraphStructure = graphStructureFromJSON('''{
        "nodes": [
            {
                "guid": "21169d37-90de-453c-86d7-c1d433f8301b", 
                "dataNode": {
                    "dataType": {
                        "class": "DataType",
                        "dataTypeName": "whiteSpace",
                        "matchFunction": "whiteSpaceMatch",
                        "dataClasses":[]
                    },
                    "parsedData": null,
                    "class": "DataNode",
                    "dataClass": null
                }, 
                "class": "GraphNode", 
                "nexts": [
                    "c8c292cc-e81f-4e36-8498-7660e5931e8d"
                ]
            }, 
            {
                "guid": "c8c292cc-e81f-4e36-8498-7660e5931e8d", 
                "dataNode": {
                    "dataType": {
                        "class": "DataType",
                        "dataTypeName": "whiteSpace",
                        "matchFunction": "whiteSpaceMatch",
                        "dataClasses":[]
                    },
                    "parsedData": null,
                    "class": "DataNode",
                    "dataClass": null
                }, 
                "class": "GraphNode", 
                "nexts": [
                    "3c8d0305-04d1-440a-bec2-547aba753793", 
                    "c8c292cc-e81f-4e36-8498-7660e5931e8d"
                ]
            }, 
            {
                "guid": "3c8d0305-04d1-440a-bec2-547aba753793", 
                "dataNode": {
                    "dataType": {
                        "class": "DataType",
                        "dataTypeName": "whiteSpace",
                        "matchFunction": "whiteSpaceMatch",
                        "dataClasses":[]
                    },
                    "parsedData": null,
                    "class": "DataNode",
                    "dataClass": null
                }, 
                "class": "GraphNode", 
                "nexts": [
                    null
                ]
            }
        ], 
        "guid": "6fbbf15d-945a-449b-861a-02c94345ce19", 
        "class": "GraphStructure", 
        "name": "word"
    }''')

genFlowGraph = flowGraphFromJSON('''{
    "graph": {
        "nodes": [
            {
                "guid": "fe086570-f285-4fd9-a2bd-d31f70263a2f", 
                "dataNode": {
                    "dataType": {
                        "matchFunction": "whiteSpaceMatch", 
                        "dataClasses": [], 
                        "class": "DataType", 
                        "dataTypeName": "whiteSpace"
                    }, 
                    "parsedData": null, 
                    "class": "DataNode", 
                    "dataClass": null
                }, 
                "class": "GraphNode", 
                "nexts": [
                    "d0bdefad-aaab-4f5e-8548-65b79087bf79"
                ]
            }, 
            {
                "guid": "d0bdefad-aaab-4f5e-8548-65b79087bf79", 
                "dataNode": {
                    "dataType": {
                        "matchFunction": "letterMatch", 
                        "dataClasses": [], 
                        "class": "DataType", 
                        "dataTypeName": "letter"
                    }, 
                    "parsedData": null, 
                    "class": "DataNode", 
                    "dataClass": null
                }, 
                "class": "GraphNode", 
                "nexts": [
                    "df9afbd0-23bb-4175-8a0d-792369bcb285", 
                    "d0bdefad-aaab-4f5e-8548-65b79087bf79"
                ]
            }, 
            {
                "guid": "df9afbd0-23bb-4175-8a0d-792369bcb285", 
                "dataNode": {
                    "dataType": {
                        "matchFunction": "whiteSpaceMatch", 
                        "dataClasses": [], 
                        "class": "DataType", 
                        "dataTypeName": "whiteSpace"
                    }, 
                    "parsedData": null, 
                    "class": "DataNode", 
                    "dataClass": null
                }, 
                "class": "GraphNode", 
                "nexts": [
                    null
                ]
            }
        ], 
        "guid": "7eaae97f-4af3-44a2-bcf2-091dbdd3eeb0", 
        "class": "GraphStructure", 
        "name": "word"
    }, 
    "class": "FlowGraph", 
    "startNodes": [
        "fe086570-f285-4fd9-a2bd-d31f70263a2f"
    ]
}''')

print(genDataNode)
#print(newWhiteSpace)
#print(genGraphStructure)
#print(str(charDataNodeB))
#print(genFlowGraph)
