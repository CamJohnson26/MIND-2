from chainGraph import ChainGraph


def pretty_chainGraphLayer(chainGraphLayer, indent=""):
    return pretty_chainGraph(chainGraphLayer.chainGraph)


def pretty_chainGraph(chainGraph, indent=""):
    rv = ""
    for n in chainGraph.graph.nodes:
        rv += str(n.dataNode.dataType.dataTypeName) + ": "
        for key in n.dataClasses.keys():
            if n.dataClasses[key]:
                rv += indent + " " + key + " : " + n.dataClasses[key].dataClassString
            else:
                rv += " " + key + " : None"
        rv += indent + "\n Parsed Data: " + pretty_parsed_data(n.dataNode.parsedData, "\t")
        rv += "\n"
    return rv


def pretty_parsed_data(parsedData, indent):
    if type(parsedData) in [str, unicode]:
        return parsedData
    elif isinstance(parsedData, ChainGraph):
        return pretty_chainGraph(parsedData, indent=indent+"\t")
    else:
        return ""
