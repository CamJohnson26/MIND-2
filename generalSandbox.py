from dataNode import DataNode
from graphNode import GraphNode
from graphStructure import GraphStructure
from flowGraph import FlowGraph
from chainGraph import ChainGraph
from chainGraphLayer import ChainGraphLayer
from chainGraphMachine import ChainGraphMachine
from dataType import DataType
from dataClass import DataClass
from Utilities.dataNodeConstructor import *
from Utilities.graphStructureConstructor import *
import Data.matchFunctions as mf

print(loadDataNode("letter.json").get_json())
