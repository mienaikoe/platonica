import {
  UNIT_HEIGHT,
  PATH_DISTANCE_60,
  TAN30,
  DEG_TO_RAD,
  SIN72,
  PATH_DISTANCE_54,
  CoordinateSystems,
} from "./constants.js";
import { drawLine, drawDot, drawPolygon, drawGroup } from "./drawSvg.js";

const opacityActive = 1;

const RED = "red";
const GREEN = "green";
const BLUE = "blue";
const BLACK = "black";
const GRAY = "#555";

/**
 * type Vertex {
    indices: [number, number], // ring, index along ring starting at bottom left
    coordinates: [number, number], // x, y
    polygons: Polygon[],
  }

  type Polygon {
    vertices: [Vertex, Vertex, Vertex], // red, blue
    paths: Polygon[],
    is_active: boolean,
  }
 *
 */

let isMouseDown = false;
const highlightedPolygonsThisRound = new Set();
document.body.addEventListener("mousedown", () => {
  isMouseDown = true;
});
document.body.addEventListener("mouseup", () => {
  isMouseDown = false;
  highlightedPolygonsThisRound.clear();
});

const renderLine = (group, from, to, isEdge) => {
  if (!from || !to) {
    return;
  }
  const line = drawLine(group, from.coordinates, to.coordinates, {
    stroke: GRAY,
    "stroke-width": 1,
  });

  if (isEdge) {
    line.setAttribute("class", "edge");
  }
};

const renderVertex = (group, vertex, isEdge) => {
  const dot = drawDot(group, vertex, {
    r: 3,
    fill: "black",
  });

  if (isEdge) {
    dot.setAttribute("class", "edge");
  }
};

const renderPolygon = (group, vertices) => {
  for (let vertex of vertices) {
    if (!vertex) {
      return;
    }
  }

  const verticesSet = new Set(vertices);

  const polygonSVG = drawPolygon(
    group,
    vertices.map((vertex) => vertex.coordinates)
  );
  const polygon = {
    vertices,
    paths: [],
    is_active: false,
  };
  vertices.forEach((vertex) => {
    vertex.polygons.push(polygon);
    polygon.paths = vertex.polygons.filter((p) => {
      return p.vertices.filter((v) => verticesSet.has(v)).length === 2;
    });
  });
  polygonSVG.addEventListener("mousemove", () => {
    if (!isMouseDown || highlightedPolygonsThisRound.has(polygonSVG)) {
      return;
    }
    if (new Set(polygonSVG.classList).has("active")) {
      polygonSVG.setAttribute("class", "");
      polygon.is_active = false;
    } else {
      polygonSVG.setAttribute("class", "active");
      polygon.is_active = true;
    }
    highlightedPolygonsThisRound.add(polygonSVG);
  });
  polygonSVG.addEventListener("click", () => {
    if (new Set(polygonSVG.classList).has("active")) {
      polygonSVG.setAttribute("class", "");
      polygon.is_active = false;
    } else {
      polygonSVG.setAttribute("class", "active");
      polygon.is_active = true;
    }
  });

  return polygon;
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
        polygons: [],
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
        vertices[ringIdx][countIdx] = {
          indices: [ringIdx, countIdx],
          coordinates,
          paths: [],
          polygons: [],
        };
        coordinates = [
          coordinates[0] + unitVector[0],
          coordinates[1] + unitVector[1],
        ];
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

  const polygonGroup = drawGroup(group);
  const lineGroup = drawGroup(group);

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

        let previousCornerVertex,
          adjacentCornerVertex,
          previousInnerVertex,
          nextInnerVertex;

        if (segmentCountIdx === 1) {
          const previousCornerVertexCountIdx =
            countIdx === 1 ? ringVertices.length - 1 : countIdx - 2;
          previousCornerVertex = ringVertices[previousCornerVertexCountIdx];
          const adjacentCornerVertexIdx = countIdx === 1 ? 0 : countIdx - 1;
          adjacentCornerVertex = ringVertices[adjacentCornerVertexIdx];
        }

        const previousRingIdx = ringIdx - 1;
        if (segmentCountIdx > 1) {
          const previousCountIdx =
            ringIdx === 1
              ? 0
              : countIdx === ringVertices.length - 1
              ? 0
              : countIdx - ((segmentIdx + 1) * verticesPerCorner - 1);
          previousInnerVertex = vertices[previousRingIdx][previousCountIdx];
        }
        if (segmentCountIdx > 0 && segmentCountIdx < verticesPerSegment - 1) {
          const nextCountIdx =
            ringIdx === 1
              ? 0
              : countIdx === ringVertices.length - 2
              ? 0
              : countIdx - ((segmentIdx + 1) * verticesPerCorner - 2);
          nextInnerVertex = vertices[previousRingIdx][nextCountIdx];
        }

        renderPolygon(polygonGroup, [
          previousCornerVertex,
          adjacentCornerVertex,
          vertex,
        ]);
        renderPolygon(polygonGroup, [
          previousCornerVertex,
          nextInnerVertex,
          vertex,
        ]);
        renderPolygon(polygonGroup, [
          previousInnerVertex,
          previousVertex,
          vertex,
        ]);
        renderPolygon(polygonGroup, [
          nextInnerVertex,
          previousInnerVertex,
          vertex,
        ]);

        renderLine(lineGroup, vertex, previousCornerVertex, false);
        renderLine(lineGroup, vertex, previousInnerVertex, false);
        renderLine(lineGroup, vertex, nextInnerVertex, false);
        renderLine(lineGroup, vertex, previousVertex, isEdge);
      }
    }
  }

  vertices.forEach((ring) => {
    ring.forEach((vertex) => {
      const isEdge = vertex.indices[0] === depth;
      renderVertex(group, vertex, isEdge);
    });
  });

  return vertices;
};

export const drawSquare = (group, depth) => {
  const coordinateSystem = CoordinateSystems.square;
  const vertices = constructVertices(coordinateSystem, depth);

  const polygonGroup = drawGroup(group);
  const lineGroup = drawGroup(group);

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

        const nextIdx = countIdx === ringVertices.length - 1 ? 0 : countIdx + 1;
        const nextVertex = vertices[ringIdx][nextIdx];
        renderLine(lineGroup, vertex, nextVertex, isEdge);

        const previousIdx = countIdx === 0 ? ringVertices - 1 : countIdx - 1;

        let directInnerVertex, nextInnerVertex;

        const previousRingIdx = ringIdx - 1;
        if (segmentCountIdx === 0) {
          const directInnerIdx =
            countIdx === 0 ? ringVertices.length - 1 : previousIdx;
          directInnerVertex = ringVertices[directInnerIdx];
        } else {
          const directInnerIdx =
            countIdx === ringVertices.length - 1
              ? 0
              : countIdx - (1 + segmentIdx * (verticesPerCorner * 2));
          directInnerVertex = vertices[previousRingIdx][directInnerIdx];
          renderLine(lineGroup, vertex, directInnerVertex, false);
        }

        if (segmentCountIdx < verticesPerSegment - 1) {
          const nextInnerIdx =
            countIdx === ringVertices.length - 2
              ? 0
              : countIdx - segmentIdx * verticesPerCorner * 2;
          nextInnerVertex = vertices[previousRingIdx][nextInnerIdx];
        }

        if (segmentCountIdx !== verticesPerSegment - 1) {
          if (segmentCountIdx >= verticesPerSegment / 2) {
            renderPolygon(polygonGroup, [
              vertex,
              nextVertex,
              directInnerVertex,
            ]);
            renderPolygon(polygonGroup, [
              nextVertex,
              nextInnerVertex,
              directInnerVertex,
            ]);
          } else {
            renderPolygon(polygonGroup, [vertex, nextVertex, nextInnerVertex]);
            renderPolygon(polygonGroup, [
              vertex,
              directInnerVertex,
              nextInnerVertex,
            ]);
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

  const polygonGroup = drawGroup(group);
  const lineGroup = drawGroup(group);

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

        const previousVertexIdx =
          countIdx === 0 ? ringVertices.length - 1 : countIdx - 1;
        const previousVertex = ringVertices[previousVertexIdx];

        const nextVertexIdx =
          countIdx === ringVertices.length - 1 ? 0 : countIdx + 1;
        const nextVertex = ringVertices[nextVertexIdx];

        const previousRingIdx = ringIdx - 1;

        const nextInnerIdx =
          ringIdx === 1
            ? 0
            : countIdx === ringVertices.length - 1
            ? 0
            : countIdx - segmentIdx * verticesPerCorner;
        const nextInnerVertex = vertices[previousRingIdx][nextInnerIdx];

        let previousInnerVertex;
        if (ringIdx > 1 && segmentCountIdx > 0) {
          const previousCountIdx =
            countIdx - (segmentIdx + 1) * verticesPerCorner;
          previousInnerVertex = vertices[previousRingIdx][previousCountIdx];
        }

        renderPolygon(polygonGroup, [nextInnerVertex, nextVertex, vertex]);
        renderPolygon(polygonGroup, [
          nextInnerVertex,
          previousInnerVertex,
          vertex,
        ]);

        renderLine(lineGroup, vertex, nextInnerVertex, false);
        renderLine(lineGroup, vertex, previousInnerVertex, false);
        renderLine(lineGroup, vertex, previousVertex, isEdge);

        renderVertex(group, vertex, isEdge);
      }
    }
  }
  renderVertex(group, vertices[0][0], false);

  return vertices;
};
