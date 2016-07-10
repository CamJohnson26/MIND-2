
def pretty_chainGraphLayer(chainGraphLayer):
    rv = ""
    for n in chainGraphLayer.chainGraph.graph.nodes:
        rv += str(n.dataNode.dataType.dataTypeName) + ": "
        if n.dataClass:
            rv += str(n.dataClass.dataClassString)
        else:
            rv += "None"
        rv += "\n"
    return rv
