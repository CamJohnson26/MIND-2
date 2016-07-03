from dataNode import DataNode
from graphNode import GraphNode
from graphStructure import GraphStructure
from flowGraph import FlowGraph
from dataGraph import DataGraph
from dataGraphLayer import DataGraphLayer
from dataGraphMachine import DataGraphMachine
from dataType import DataType
from dataClass import DataClass
from Utilities.dataNodeConstructor import *
from Utilities.graphStructureConstructor import *
import Data.matchFunctions as mf

print(loadDataNode("letter.json").get_json())
