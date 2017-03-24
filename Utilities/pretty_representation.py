from chainGraph import ChainGraph


def pretty_chainGraphLayer(chainGraphLayer, indent=""):
    return pretty_chainGraph(chainGraphLayer.chainGraph)


def pretty_chainGraph(chainGraph, indent=""):
    rv = ""
    for n in chainGraph.graph.nodes:
        rv += indent + str(n.dataType.dataTypeName) + ": "
        for key in n.dataClasses.keys():
            if n.dataClasses[key]:
                rv += " " + key + " : " + n.dataClasses[key].dataClassString
            else:
                rv += " " + key + " : None"
        rv += " Parsed Data: \n" + pretty_parsed_data(n.parsedData, "\t")
        rv += "\n"
    return rv


def pretty_parsed_data(parsedData, indent):
    if type(parsedData) in [str]:
        return parsedData
    elif isinstance(parsedData, ChainGraph):
        return pretty_chainGraph(parsedData, indent=indent+"\t")
    else:
        return ""
