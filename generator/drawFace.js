import {
  UNIT_HEIGHT,
  PATH_DISTANCE_60,
  TAN30,
  DEG_TO_RAD,
  SIN72,
  PATH_DISTANCE_54,
  CoordinateSystems,
} from "./constants.js";
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
    indices: [number, number], // ring, index along ring starting at bottom left
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

const constructVertices = (coordinateSystem, depth) => {
  const {
    numSegments,
    verticesPerSegmentPerRing,
    ringShiftUnit,
    segmentUnitVectors,
  } = coordinateSystem;

  // equilateral triangle
  const center = [-ringShiftUnit[0] * depth, -ringShiftUnit[1] * depth];

  // construct vertices
  const vertices = [
    [
      {
        indices: [0, 0],
        coordinates: center,
        paths: [],
        type: null,
      },
    ], // center has one vertex
  ]; // Vertex[][]
  for (let ringIdx = 1; ringIdx <= depth; ringIdx++) {
    const ringShift = [ringShiftUnit[0] * ringIdx, ringShiftUnit[1] * ringIdx];
    const verticesPerSegment = verticesPerSegmentPerRing * ringIdx;
    vertices[ringIdx] = [];
    let coordinates = [center[0] + ringShift[0], center[1] + ringShift[1]];
    for (let segmentIdx = 0; segmentIdx < numSegments; segmentIdx++) {
      const unitVector = segmentUnitVectors[segmentIdx];
      for (
        let segmentCountIdx = 0;
        segmentCountIdx < verticesPerSegment;
        segmentCountIdx++
      ) {
        const countIdx = segmentIdx * verticesPerSegment + segmentCountIdx;
        coordinates = [
          coordinates[0] + unitVector[0],
          coordinates[1] + unitVector[1],
        ];
        vertices[ringIdx][countIdx] = {
          indices: [ringIdx, countIdx],
          coordinates,
          paths: [],
          type: null,
        };
      }
    }
  }

  return vertices;
};

export const drawTriangle = (group, depth) => {
  const coordinateSystem = CoordinateSystems.triangle;
  const vertices = constructVertices(coordinateSystem, depth);

  const { numSegments, verticesPerSegmentPerRing, verticesPerCorner } =
    coordinateSystem;

  for (let ringIdx = 1; ringIdx <= depth; ringIdx++) {
    const ringVertices = vertices[ringIdx];
    const verticesPerSegment = verticesPerSegmentPerRing * ringIdx;
    const isEdge = ringIdx === depth;
    for (let segmentIdx = 0; segmentIdx < numSegments; segmentIdx++) {
      for (
        let segmentCountIdx = 0;
        segmentCountIdx < verticesPerSegment;
        segmentCountIdx++
      ) {
        const countIdx = segmentIdx * verticesPerSegment + segmentCountIdx;
        const vertex = ringVertices[countIdx];

        const previousVertexCountIdx =
          countIdx === 0 ? ringVertices.length - 1 : countIdx - 1;
        const previousVertex = vertices[ringIdx][previousVertexCountIdx];
        createPath(group, vertex, previousVertex, RED, isEdge);

        if (segmentCountIdx === 0) {
          const previousCornerVertexCountIdx =
            countIdx === 0 ? ringVertices.length - 2 : countIdx - 2;
          const previousCornerVertex =
            vertices[ringIdx][previousCornerVertexCountIdx];
          createPath(group, vertex, previousCornerVertex, GREEN, false);
        }

        const previousRingIdx = ringIdx - 1;
        if (segmentCountIdx > 0 && segmentCountIdx < verticesPerSegment - 1) {
          const previousCountIdx =
            ringIdx === 1
              ? 0
              : countIdx === 1
              ? numSegments * verticesPerSegmentPerRing * previousRingIdx - 1
              : countIdx - ((segmentIdx + 1) * verticesPerCorner - 1);
          const previousInnerVertex =
            vertices[previousRingIdx][previousCountIdx];

          if (previousInnerVertex) {
            createPath(group, vertex, previousInnerVertex, BLUE, false);
          }
        }
        if (
          ringIdx > 1 &&
          segmentCountIdx > -1 &&
          segmentCountIdx < verticesPerSegment - 2
        ) {
          const nextCountIdx =
            countIdx === 0
              ? numSegments * verticesPerSegmentPerRing * previousRingIdx - 1
              : countIdx - ((segmentIdx + 1) * verticesPerCorner - 2);
          const nextInnerVertex = vertices[previousRingIdx][nextCountIdx];
          if (nextInnerVertex) {
            createPath(group, vertex, nextInnerVertex, BLUE, false);
          }
        }

        renderVertex(group, vertex, isEdge);
      }
    }
  }
  renderVertex(group, vertices[0][0], false);

  return vertices;
};

export const drawSquare = (group, depth) => {
  const coordinateSystem = CoordinateSystems.square;
  const vertices = constructVertices(coordinateSystem, depth);

  const { numSegments, verticesPerSegmentPerRing, verticesPerCorner } =
    coordinateSystem;

  for (let ringIdx = 1; ringIdx <= depth; ringIdx++) {
    const ringVertices = vertices[ringIdx];
    const verticesPerSegment = verticesPerSegmentPerRing * ringIdx;
    const isEdge = ringIdx === depth;
    for (let segmentIdx = 0; segmentIdx < numSegments; segmentIdx++) {
      for (
        let segmentCountIdx = 0;
        segmentCountIdx < verticesPerSegment;
        segmentCountIdx++
      ) {
        const countIdx = segmentIdx * verticesPerSegment + segmentCountIdx;
        const vertex = ringVertices[countIdx];

        const previousVertexCountIdx =
          countIdx === 0 ? ringVertices.length - 1 : countIdx - 1;
        const previousVertex = vertices[ringIdx][previousVertexCountIdx];
        createPath(group, vertex, previousVertex, RED, isEdge);

        const previousRingIdx = ringIdx - 1;
        if (segmentCountIdx < verticesPerSegment - 1) {
          const previousCountIdx =
            ringIdx === 1
              ? 0
              : countIdx === 0
              ? numSegments * verticesPerSegmentPerRing * previousRingIdx - 1
              : countIdx - (1 + segmentIdx * (verticesPerCorner * 2));
          const previousInnerVertex =
            vertices[previousRingIdx][previousCountIdx];
          if (previousInnerVertex) {
            createPath(group, vertex, previousInnerVertex, BLUE, false);
          }
        }

        renderVertex(group, vertex, isEdge);
      }
    }
  }

  renderVertex(group, vertices[0][0], false);

  return vertices;
};

export const drawPentagon = (group, depth) => {
  const coordinateSystem = CoordinateSystems.pentagon;

  const vertices = constructVertices(coordinateSystem, depth);

  const { numSegments, verticesPerSegmentPerRing, verticesPerCorner } =
    coordinateSystem;

  for (let ringIdx = 1; ringIdx <= depth; ringIdx++) {
    const ringVertices = vertices[ringIdx];
    const verticesPerSegment = verticesPerSegmentPerRing * ringIdx;
    const isEdge = ringIdx === depth;
    for (let segmentIdx = 0; segmentIdx < numSegments; segmentIdx++) {
      for (
        let segmentCountIdx = 0;
        segmentCountIdx < verticesPerSegment;
        segmentCountIdx++
      ) {
        const countIdx = segmentIdx * verticesPerSegment + segmentCountIdx;
        const vertex = ringVertices[countIdx];

        const previousVertexCountIdx =
          countIdx === 0 ? ringVertices.length - 1 : countIdx - 1;
        const previousVertex = vertices[ringIdx][previousVertexCountIdx];
        createPath(group, vertex, previousVertex, RED, isEdge);

        const previousRingIdx = ringIdx - 1;

        const previousCountIdx =
          ringIdx === 1
            ? 0
            : countIdx === 0
            ? numSegments * verticesPerSegmentPerRing * previousRingIdx - 1
            : countIdx - (segmentIdx + 1) * verticesPerCorner;
        const previousInnerVertex = vertices[previousRingIdx][previousCountIdx];

        if (previousInnerVertex) {
          createPath(group, vertex, previousInnerVertex, BLUE, false);
        }

        if (ringIdx > 1 && segmentCountIdx < verticesPerSegment - 1) {
          const nextCountIdx = countIdx - segmentIdx * verticesPerCorner;
          const nextInnerVertex = vertices[previousRingIdx][nextCountIdx];
          if (nextInnerVertex) {
            createPath(group, vertex, nextInnerVertex, BLUE, false);
          }
        }

        renderVertex(group, vertex, isEdge);
      }
    }
  }
  renderVertex(group, vertices[0][0], false);

  return vertices;
};
