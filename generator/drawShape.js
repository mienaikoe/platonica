import { UNIT_HEIGHT, UNIT_WIDTH, TAN30, SVG_PADDING } from "./constants.js";
import { drawLine, drawDot, drawGroup } from "./drawSvg.js";

const strokeWidthInactive = 5;
const opacityInactive = 0.3;
const strokeWidthActive = 9;
const opacityActive = 1;
const colorActive = "black";

const RED = "red";
const GREEN = "green";
const BLUE = "blue";

/**
 * type Vertex {
    indices: [number, number], // red, blue
    coordinates: [number, number], // x, y
    paths: Path[],
    type: "hole" | "start" | null
  }

  type Path {
    from: [number, number], // red, blue
    to: [number, number], // red, blue
    active: boolean,
  }
 *
 */

const toggleEdge = (edge, line) => {
  if (edge.active) {
    edge.active = false;
    line.setAttribute("stroke-width", strokeWidthInactive);
    line.setAttribute("opacity", opacityInactive);
    line.setAttribute("stroke", line.getAttribute("data-color-default"));
  } else {
    edge.active = true;
    line.setAttribute("stroke-width", strokeWidthActive);
    line.setAttribute("opacity", opacityActive);
    line.setAttribute("stroke", colorActive);
  }
};

const toggleVertex = (vertex, dot) => {
  switch (vertex.type) {
    case "hole":
      vertex.type = "start";
      dot.setAttribute("stroke", "goldenrod");
      dot.setAttribute("fill", "goldenrod");
      break;
    case "start":
      vertex.type = null;
      dot.setAttribute("stroke", "black");
      dot.setAttribute("fill", "black");
      break;
    default:
      vertex.type = "hole";
      dot.setAttribute("stroke", "black");
      dot.setAttribute("fill", "white");
      break;
  }
};

const createPath = (svgGroup, from, to, color, depth) => {
  const newPath = {
    indices: [from.indices, to.indices],
    active: false,
  };

  const pathKeyA = newPath.indices.toString();
  const pathKeyB = newPath.indices.reverse().toString();

  const existingFrom = from.paths.find((path) => {
    const pathKey = path.indices.toString();
    return pathKey === pathKeyA || pathKey === pathKeyB;
  });
  if (!existingFrom) {
    from.paths.push(newPath);
  }

  const existingTo = to.paths.find((path) => {
    const pathKey = path.indices.toString();
    return pathKey === pathKeyA || pathKey === pathKeyB;
  });
  if (!existingTo) {
    to.paths.push(newPath);
  }

  const line = drawLine(svgGroup, from.coordinates, to.coordinates, {
    stroke: color,
    "data-color-default": color,
    "stroke-width": strokeWidthInactive,
    opacity: opacityInactive,
  });

  const isEdgePiece =
    (from.indices[0] === 0 && to.indices[0] === 0) || // red
    (from.indices[1] === 0 && to.indices[1] === 0) || // blue
    (from.indices[0] + from.indices[1] === depth - 1 &&
      to.indices[0] + to.indices[1] === depth - 1); // green

  if (isEdgePiece) {
    line.setAttribute("class", "edge");
  } else {
    line.addEventListener("click", () => {
      toggleEdge(newPath, line);
    });
  }
};

const renderVertex = (group, vertex, depth) => {
  const dot = drawDot(group, vertex, {
    r: 6,
    fill: "black",
    "stroke-width": 4,
    stroke: "black",
  });

  const isEdgePiece =
    vertex.indices[0] === 0 || // red
    vertex.indices[1] === 0 || // blue
    vertex.indices[0] + vertex.indices[1] === depth - 1; // green

  if (isEdgePiece) {
    dot.setAttribute("class", "edge");
  } else {
    dot.addEventListener("click", () => {
      toggleVertex(vertex, dot);
    });
  }
};

const drawTriangle = (group, depth) => {
  // construct vertices
  const vertices = []; // Vertex[][]
  for (let redIdx = 0; redIdx < depth; redIdx++) {
    vertices[redIdx] = [];
    const redShift = redIdx * UNIT_WIDTH;
    const vertexCount = depth - redIdx - 1;
    for (let blueIdx = 0; blueIdx <= vertexCount; blueIdx++) {
      const y = blueIdx * UNIT_HEIGHT;
      const x = TAN30 * y + redShift;

      vertices[redIdx][blueIdx] = {
        indices: [redIdx, blueIdx],
        coordinates: [x, y],
        paths: [],
        type: null,
      };
    }
  }

  for (let redIdx = 0; redIdx < vertices.length; redIdx++) {
    const redVertices = vertices[redIdx];
    for (let blueIdx = 0; blueIdx < redVertices.length; blueIdx++) {
      const vertex = redVertices[blueIdx];

      const redVertex = redVertices[blueIdx + 1];
      if (redVertex) {
        createPath(group, vertex, redVertex, RED, depth);
      }

      const greenVertices = vertices[redIdx + 1];
      const greenVertex = greenVertices && greenVertices[blueIdx - 1];
      if (greenVertex) {
        createPath(group, vertex, greenVertex, GREEN, depth);
      }

      const blueVertices = vertices[redIdx + 1];
      const blueVertex = blueVertices && blueVertices[blueIdx];
      if (blueVertex) {
        createPath(group, vertex, blueVertex, BLUE, depth);
      }

      renderVertex(group, vertex, depth);
    }
  }

  return vertices;
};

const drawTetrahedron = (svg, depth) => {
  const midpoint = [
    svg.getAttribute("width") / 2,
    svg.getAttribute("height") / 2,
  ];

  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(-${SVG_PADDING}, -${SVG_PADDING}) rotate(180, ${midpoint[0]}, ${midpoint[1]})`
  );

  const fullPoint = [UNIT_WIDTH * (depth - 1), UNIT_HEIGHT * (depth - 1)];
  const segmentVertices = {};

  const triangleA = drawGroup(containerGroup);
  segmentVertices.A = drawTriangle(triangleA, depth);

  const triangleB = drawGroup(containerGroup);
  triangleB.setAttribute("transform", `translate(${fullPoint[0]}, 0)`);
  segmentVertices.B = drawTriangle(triangleB, depth);

  const triangleC = drawGroup(containerGroup);
  triangleC.setAttribute(
    "transform",
    `
    translate(${fullPoint[0] / 2} ${fullPoint[1]})
    rotate(180 ${fullPoint[0] / 2} 0)
    `
  );
  segmentVertices.C = drawTriangle(triangleC, depth);

  const triangleD = drawGroup(containerGroup);
  triangleD.setAttribute(
    "transform",
    `
    translate(${fullPoint[0] / 2}, ${fullPoint[1]})
    `
  );
  segmentVertices.D = drawTriangle(triangleD, depth);

  return segmentVertices;
};

const drawOctahedron = (svg, depth) => {
  const midpoint = [
    svg.getAttribute("width") / 2,
    svg.getAttribute("height") / 2,
  ];

  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(-${SVG_PADDING}, -${SVG_PADDING}) rotate(180, ${midpoint[0]}, ${midpoint[1]})`
  );

  const fullPoint = [UNIT_WIDTH * (depth - 1), UNIT_HEIGHT * (depth - 1)];
  const segmentVertices = {};

  const segmentPairs = [
    ["A", "B"],
    ["C", "D"],
    ["E", "F"],
    ["G", "H"],
  ];
  segmentPairs.forEach((pair, ix) => {
    const translateX = fullPoint[0] * ix;

    const bottomTriangle = drawGroup(containerGroup);
    bottomTriangle.setAttribute(
      "transform",
      `translate(-${translateX}, 0) rotate(180 ${
        translateX + fullPoint[0] / 2
      } ${fullPoint[1] / 2})`
    );
    segmentVertices[pair[0]] = drawTriangle(bottomTriangle, depth);

    const topTriangle = drawGroup(containerGroup);
    topTriangle.setAttribute(
      "transform",
      `translate(${translateX} ${fullPoint[1]})`
    );
    segmentVertices[pair[1]] = drawTriangle(topTriangle, depth);
  });

  return segmentVertices;
};

const drawIcosahedron = (svg, depth) => {
  const midpoint = [
    svg.getAttribute("width") / 2,
    svg.getAttribute("height") / 2,
  ];

  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(-${SVG_PADDING}, -${SVG_PADDING}) rotate(180, ${midpoint[0]}, ${midpoint[1]})`
  );

  const fullPoint = [UNIT_WIDTH * (depth - 1), UNIT_HEIGHT * (depth - 1)];
  const segmentVertices = {};

  const segmentQuads = [
    ["A", "B", "C", "D"],
    ["E", "F", "G", "H"],
    ["I", "J", "K", "L"],
    ["M", "N", "O", "P"],
    ["Q", "R", "S", "T"],
  ];
  segmentQuads.forEach((quad, ix) => {
    const translateX = fullPoint[0] * ix;

    const bottomTriangle = drawGroup(containerGroup);
    bottomTriangle.setAttribute(
      "transform",
      `translate(-${translateX}, 0)
        rotate(180 ${translateX + fullPoint[0] / 2} ${fullPoint[1] / 2})`
    );
    segmentVertices[quad[0]] = drawTriangle(bottomTriangle, depth);

    const midBottomTriangle = drawGroup(containerGroup);
    midBottomTriangle.setAttribute(
      "transform",
      `translate(${translateX} ${fullPoint[1]})`
    );
    segmentVertices[quad[1]] = drawTriangle(midBottomTriangle, depth);

    const midTopTriangle = drawGroup(containerGroup);
    midTopTriangle.setAttribute(
      "transform",
      `translate(${fullPoint[0] / 2 - translateX} -${fullPoint[1]})
      rotate(180 ${translateX + fullPoint[0] / 2} ${fullPoint[1] * 1.5} )
      `
    );
    segmentVertices[quad[1]] = drawTriangle(midTopTriangle, depth);

    const topTriangle = drawGroup(containerGroup);
    topTriangle.setAttribute(
      "transform",
      `translate(${translateX + fullPoint[0] / 2} ${2 * fullPoint[1]})`
    );
    segmentVertices[quad[1]] = drawTriangle(topTriangle, depth);
  });

  return segmentVertices;
};

const drawShape = {
  tetrahedron: drawTetrahedron,
  octahedron: drawOctahedron,
  icosahedron: drawIcosahedron,
};

export const shapeScales = {
  tetrahedron: [2, 2],
  octahedron: [4, 2],
  icosahedron: [5.5, 3],
};

export default drawShape;
