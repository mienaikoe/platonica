export const drawGroup = (svgParent) => {
  const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
  svgParent.appendChild(group);
  return group;
};

export const drawLine = (svgParent, from, to, attributes) => {
  const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
  line.setAttribute("x1", from[0]);
  line.setAttribute("y1", from[1]);
  line.setAttribute("x2", to[0]);
  line.setAttribute("y2", to[1]);
  for (let attribute in attributes) {
    line.setAttribute(attribute, attributes[attribute]);
  }
  svgParent.appendChild(line);
  return line;
};

export const drawDot = (svgParent, vertex, attributes) => {
  const position = vertex.coordinates;
  const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  dot.setAttribute("cx", position[0]);
  dot.setAttribute("cy", position[1]);
  for (let attribute in attributes) {
    dot.setAttribute(attribute, attributes[attribute]);
  }
  svgParent.appendChild(dot);

  const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
  label.setAttribute("x", position[0]);
  label.setAttribute("y", position[1] - 6);
  label.innerHTML = vertex.indices.join(",");
  svgParent.appendChild(label);

  return dot;
};

export const drawPolygon = (svgParent, vertices, attributes) => {
  const polygon = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "polygon"
  );
  const points = vertices.map((vertex) => vertex.join(", ")).join("   ");
  polygon.setAttribute("points", points);
  for (let attribute in attributes) {
    polygon.setAttribute(attribute, attributes[attribute]);
  }
  svgParent.appendChild(polygon);
  return polygon;
};
