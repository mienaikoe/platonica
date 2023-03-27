import { UNIT_HEIGHT, UNIT_WIDTH, TAN30 } from "./constants.js";
import { drawLine, drawDot } from "./drawSvg.js";

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

const createPath = (svgGroup, from, to, color, isEdge) => {
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

  if (isEdge) {
    line.setAttribute("class", "edge");
  } else {
    line.addEventListener("click", () => {
      toggleEdge(newPath, line);
    });
  }
};

const renderVertex = (group, vertex, isEdge) => {
  const dot = drawDot(group, vertex, {
    r: 6,
    fill: "black",
    "stroke-width": 4,
    stroke: "black",
  });

  if (isEdge) {
    dot.setAttribute("class", "edge");
  } else {
    dot.addEventListener("click", () => {
      toggleVertex(vertex, dot);
    });
  }
};

const CoordinateSystems = {
  triangle: {
    isPathEdge: (vertexA, vertexB, depth) => {
      return (
        (vertexA.indices[0] === 0 && vertexB.indices[0] === 0) ||
        (vertexA.indices[1] === 0 && vertexB.indices[1] === 0) ||
        (vertexA.indices[0] + vertexA.indices[1] === depth - 1 &&
          vertexB.indices[0] + vertexA.indices[1] === depth - 1)
      );
    },
    isVertexEdge: (vertex, depth) => {
      return (
        vertex.indices[0] === 0 || // red
        vertex.indices[1] === 0 || // blue
        vertex.indices[0] + vertex.indices[1] === depth - 1
      ); // green
    },
  },
  square: {
    isPathEdge: (vertexA, vertexB, depth) => {
      return (
        (vertexA.indices[0] === 0 && vertexB.indices[0] === 0) ||
        (vertexA.indices[1] === 0 && vertexB.indices[1] === 0) ||
        (vertexA.indices[0] === depth - 1 &&
          vertexB.indices[0] === depth - 1) ||
        (vertexA.indices[1] === depth - 1 && vertexB.indices[1] === depth - 1)
      );
    },
    isVertexEdge: (vertex, depth) => {
      return (
        vertex.indices[0] === 0 ||
        vertex.indices[1] === 0 ||
        vertex.indices[0] === depth - 1 ||
        vertex.indices[1] === depth - 1
      );
    },
  },
};

export const drawTriangle = (group, depth) => {
  const coordinateSystem = CoordinateSystems.triangle;

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
        createPath(
          group,
          vertex,
          redVertex,
          RED,
          coordinateSystem.isPathEdge(vertex, redVertex, depth)
        );
      }

      const greenVertices = vertices[redIdx + 1];
      const greenVertex = greenVertices && greenVertices[blueIdx - 1];
      if (greenVertex) {
        createPath(
          group,
          vertex,
          greenVertex,
          GREEN,
          coordinateSystem.isPathEdge(vertex, greenVertex, depth)
        );
      }

      const blueVertices = vertices[redIdx + 1];
      const blueVertex = blueVertices && blueVertices[blueIdx];
      if (blueVertex) {
        createPath(
          group,
          vertex,
          blueVertex,
          BLUE,
          coordinateSystem.isPathEdge(vertex, blueVertex, depth)
        );
      }

      renderVertex(
        group,
        vertex,
        depth,
        coordinateSystem.isVertexEdge(vertex, depth)
      );
    }
  }

  return vertices;
};

export const drawSquare = (group, depth) => {
  const coordinateSystem = CoordinateSystems.square;

  // construct vertices
  const vertices = []; // Vertex[][]
  for (let redIdx = 0; redIdx < depth; redIdx++) {
    vertices[redIdx] = [];
    for (let blueIdx = 0; blueIdx < depth; blueIdx++) {
      vertices[redIdx][blueIdx] = {
        indices: [redIdx, blueIdx],
        coordinates: [redIdx * UNIT_WIDTH, blueIdx * UNIT_WIDTH],
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
        createPath(
          group,
          vertex,
          redVertex,
          RED,
          coordinateSystem.isPathEdge(vertex, redVertex, depth)
        );
      }

      const blueVertices = vertices[redIdx + 1];
      const blueVertex = blueVertices && blueVertices[blueIdx];
      if (blueVertex) {
        createPath(
          group,
          vertex,
          blueVertex,
          BLUE,
          coordinateSystem.isPathEdge(vertex, blueVertex, depth)
        );
      }

      renderVertex(
        group,
        vertex,
        depth,
        coordinateSystem.isVertexEdge(vertex, depth)
      );
    }
  }

  return vertices;
};
