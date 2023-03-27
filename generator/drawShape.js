const DEG_TO_RAD = Math.PI / 180;

const depthDistance = 30; // pixels between each line, also triangle height
const depthDistance60 = depthDistance / Math.sin(60 * DEG_TO_RAD);

const width = 800;
const height = 600;

const RED = "#FAA";
const GREEN = "#AFA";
const BLUE = "#AAF";

const drawLine = (svg, color, from, to) => {
  const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
  line.setAttribute("x1", from[0]);
  line.setAttribute("y1", height - from[1]);
  line.setAttribute("x2", to[0]);
  line.setAttribute("y2", height - to[1]);
  line.setAttribute("stroke", color);
  line.setAttribute("stroke-width", "1");
  svg.appendChild(line);
};

const drawDot = (svg, position) => {
  const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  dot.setAttribute("cx", position[0]);
  dot.setAttribute("cy", height - position[1]);
  dot.setAttribute("r", "2");
  svg.appendChild(dot);
};

const tetrahedron = (svg, depth) => {
  const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
  group.setAttribute("transform", "translate(20, -20)");
  svg.appendChild(group);

  // construct vertices
  const vertexGroups = [];
  for (let greenIdx = 0; greenIdx <= depth; greenIdx++) {
    vertexGroups[greenIdx] = [];
    const shift60 = greenIdx * depthDistance60;
    const vertexCount = depth - greenIdx;
    for (let redIdx = 0; redIdx <= vertexCount; redIdx++) {
      const yToX = Math.tan(30 * DEG_TO_RAD);
      const coordinates = [
        yToX * redIdx * depthDistance + shift60,
        redIdx * depthDistance,
      ];
      vertexGroups[greenIdx][redIdx] = coordinates;
    }
  }

  for (
    let vertexGroupIx = 0;
    vertexGroupIx < vertexGroups.length;
    vertexGroupIx++
  ) {
    const vertices = vertexGroups[vertexGroupIx];
    for (let vertexIx = 0; vertexIx < vertices.length; vertexIx++) {
      const vertex = vertices[vertexIx];

      const redVertex = vertices[vertexIx + 1];
      if (redVertex) {
        drawLine(group, RED, vertex, redVertex);
      }

      const greenVertexGroup = vertexGroups[vertexGroupIx + 1];
      const greenVertex = greenVertexGroup && greenVertexGroup[vertexIx - 1];
      if (greenVertex) {
        drawLine(group, GREEN, vertex, greenVertex);
      }

      const blueVertexGroup = vertexGroups[vertexGroupIx + 1];
      const blueVertex = blueVertexGroup && blueVertexGroup[vertexIx];
      if (blueVertex) {
        drawLine(group, BLUE, vertex, blueVertex);
      }

      drawDot(group, vertex);
    }
  }
};

const drawShape = {
  tetrahedron,
};

export default drawShape;
