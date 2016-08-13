
def pretty_chainGraphLayer(chainGraphLayer):
    rv = ""
    for n in chainGraphLayer.chainGraph.graph.nodes:
        rv += str(n.dataNode.dataType.dataTypeName) + ": "
        if n.dataClasses.get("dataIndex"):
            rv += str(n.dataClasses["dataIndex"].dataClassString)
        else:
            rv += "None"
        rv += "\n"
    return rv
