
window.onload = function() {
  populateFiles();
  openFile("data_index.txt", function(r){
    console.log(r)
  })
  var width = 1500,
    height = 900
var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var force = d3.layout.force()
    .gravity(.05)
    .distance(100)
    .charge(-100)
    .size([width, height]);


  let dataTypeJson = {
    "matchFunction": "charMatch", 
    "dataClasses": {
        "dataIndex": null
    }, 
    "class": "DataType", 
    "dataTypeName": "char"
  }

  let dataNodeJson = {
    "dataType": "adjective.json", 
    "parsedData": null, 
    "class": "DataNode", 
    "dataClasses": {}
}

  //let graphJson = dataTypeToNodesAndLinks(dataTypeJson)
  let graphJson = dataTypeToNodesAndLinks(dataTypeJson);
  console.log(graphJson)

  let nodes =  []

  Object.keys(graphJson.nodes).forEach(function(e, i) {
    nodes.push(graphJson.nodes[e]);
    graphJson.nodes[e].index = i;
  })
  console.log(nodes)
  var links = []

  graphJson.links.forEach(function(e) {
    let source = graphJson.nodes[e.source.id].index;
    let target = graphJson.nodes[e.target.id].index;
    e.source = source;
    e.target = target;
    links.push(e)
  })

  console.log(links)

  force
      .nodes(nodes)
      .links(links)
      .start();

  var link = svg.selectAll(".link")
      .data(links)
    .enter().append("line")
      .attr("class", "link")
    .style("stroke-width", function(d) { return Math.sqrt(d.weight); });

  var node = svg.selectAll(".node")
      .data(nodes)
    .enter().append("g")
      .attr("class", "node")
      .call(force.drag);

  node.append("circle")
      .attr("r","15");

  node.append("text")
      .attr("dx", 12)
      .attr("dy", ".35em")
      .text(function(d) { return d.class + ": " + d.name });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
}

function populateFiles() {
  let node = document.createTextNode("Water"); 
  document.getElementById("sidebar").appendChild(node);
}

function openFile(file, callback) {
  var r = new XMLHttpRequest();
  r.onload = function() {
    callback(this.responseText)
  };
  r.open("get", file, true);
  r.send();
}

function dataNodeToNodesAndLinks(inputJson) {
  let newDataNodeNode = createNode("", "DataNode")
  var rv = {
    nodes: {
    },
    links: []
  };
  rv.nodes[newDataTypeNode.id] = newDataNodeNode;
  for (var key in inputJson.dataClasses) {
    let newDataClassNode = createNode(inputJson.dataClasses[key], "DataClass")
    rv.nodes[newDataClassNode.id] = newDataClassNode;
    rv.links.push(createLink(newDataTypeNode, newDataClassNode, key))
  }

  return rv;
}

function dataTypeToNodesAndLinks(inputJson) {
  let newDataTypeNode = createNode(inputJson.dataTypeName, "DataType")
  var rv = {
    nodes: {
    },
    links: []
  };
  rv.nodes[newDataTypeNode.id] = newDataTypeNode;
  for (var key in inputJson.dataClasses) {
    let newDataClassNode = createNode(inputJson.dataClasses[key], "DataClass")
    rv.nodes[newDataClassNode.id] = newDataClassNode;
    rv.links.push(createLink(newDataTypeNode, newDataClassNode, key))
  }
  return rv;
}

function createNode(name, iclass) {
  let rv = {
    name: name,
    class: iclass,
    id: getNewGuid()
  };
  return rv;
}

function createLink(source, target, name) {
  let rv = {
    source,
    target,
    name,
    id: getNewGuid()
  };
  return rv;
}

function drawDataType() {

}

function getNewGuid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
      return v.toString(16);
    });
}

// {
//   "nodes":[
//     {"name":"node1","class":1},
//     {"name":"node2","group":2},
//     {"name":"node3","group":2},
//     {"name":"node4","group":3}
//   ],
//   "links":[
//     {"source":2,"target":1,"weight":1},
//     {"source":0,"target":2,"weight":3}
//   ]
// }