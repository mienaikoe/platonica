import {
  COS72,
  UNIT_HEIGHT,
  PATH_DISTANCE_60,
  SVG_PADDING,
  PATH_DISTANCE_54,
  CoordinateSystems,
  SIN36,
  COS54,
} from "./constants.js";
import { drawGroup } from "./drawSvg.js";
import { drawPentagon, drawSquare, drawTriangle } from "./drawFace.js";

const drawTetrahedron = (svg, depth) => {
  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(${SVG_PADDING}, ${SVG_PADDING})`
  );

  const { verticesPerSegmentPerRing } = CoordinateSystems.triangle;

  const fullPoint = [
    PATH_DISTANCE_60 * verticesPerSegmentPerRing * depth,
    UNIT_HEIGHT * verticesPerSegmentPerRing * depth,
  ];
  const segmentVertices = {};

  const triangleA = drawGroup(containerGroup);
  segmentVertices.A = drawTriangle(triangleA, depth);

  const triangleB = drawGroup(containerGroup);
  triangleB.setAttribute("transform", `translate(${fullPoint[0]}, 0)`);
  segmentVertices.B = drawTriangle(triangleB, depth);

  const triangleC = drawGroup(containerGroup);
  triangleC.setAttribute(
    "transform",
    `rotate(180 0 0) translate(-${fullPoint[0] * 1.5} -${fullPoint[1]})`
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

const drawCube = (svg, depth) => {
  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(${SVG_PADDING}, ${SVG_PADDING})`
  );

  const coordinateSystem = CoordinateSystems.square;

  const fullPoint =
    UNIT_HEIGHT * (coordinateSystem.verticesPerSegmentPerRing * depth);
  const segmentTranslations = {
    A: [0, 1],
    B: [1, 0],
    C: [1, 1],
    D: [1, 2],
    E: [2, 1],
    F: [3, 1],
  };
  const segmentVertices = {};

  for (let segmentKey in segmentTranslations) {
    const translations = segmentTranslations[segmentKey];
    const square = drawGroup(containerGroup);
    square.setAttribute(
      "transform",
      `
      translate(${fullPoint * translations[0]}, ${fullPoint * translations[1]})
    `
    );
    segmentVertices[segmentKey] = drawSquare(square, depth);
  }

  return segmentVertices;
};

const drawOctahedron = (svg, depth) => {
  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(${SVG_PADDING}, ${SVG_PADDING})`
  );

  const { verticesPerSegmentPerRing } = CoordinateSystems.triangle;

  const fullPoint = [
    PATH_DISTANCE_60 * verticesPerSegmentPerRing * depth,
    UNIT_HEIGHT * verticesPerSegmentPerRing * depth,
  ];

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
  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(${SVG_PADDING}, ${SVG_PADDING})`
  );

  const { verticesPerSegmentPerRing } = CoordinateSystems.triangle;

  const fullPoint = [
    PATH_DISTANCE_60 * verticesPerSegmentPerRing * depth,
    UNIT_HEIGHT * verticesPerSegmentPerRing * depth,
  ];

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

const drawDodecahedron = (svg, depth) => {
  const { verticesPerSegmentPerRing } = CoordinateSystems.pentagon;

  const subTriangleWidth = PATH_DISTANCE_54 * verticesPerSegmentPerRing * depth;
  const subTriangleHeight = UNIT_HEIGHT * depth;
  const subTriangleLeg = subTriangleWidth / (2 * COS54);
  const armWidth = subTriangleWidth * COS72;
  const headHeight = subTriangleWidth * SIN36;
  const fullPoint = [
    subTriangleWidth + 2 * armWidth,
    subTriangleHeight + subTriangleLeg,
  ];

  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(${SVG_PADDING + armWidth}, ${SVG_PADDING})`
  );

  const segmentVertices = {};

  const segmentGroups = [
    ["A", "B", "C", "D", "E", "F"],
    ["G", "H", "I", "J", "K", "L"],
  ];

  // https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F62%2F80%2F2e%2F62802e0f219129259ab292b55b673d4e.jpg&f=1&nofb=1&ipt=03bf02cdd68822ca120e2aabb9efde9100008c829918f8acde46a79298333779&ipo=images
  segmentGroups.forEach((segmentGroup, ix) => {
    const segmentGroupGroup = drawGroup(containerGroup);
    if (ix === 1) {
      const rotate = `rotate(180 ${subTriangleWidth * 1.5 + armWidth} ${
        (3 * fullPoint[1] - headHeight) / 2
      })`;
      const translate = `translate(-${
        2 * fullPoint[0] + subTriangleWidth - armWidth
      }, 0)`;
      segmentGroupGroup.setAttribute("transform", `${rotate} ${translate}`);
    }

    const bottomPentagon = drawGroup(segmentGroupGroup);
    bottomPentagon.setAttribute(
      "transform",
      `translate(${subTriangleWidth + armWidth}, ${
        2 * fullPoint[1] - headHeight
      })`
    );
    segmentVertices[segmentGroup[0]] = drawPentagon(bottomPentagon, depth);

    const leftPentagon = drawGroup(segmentGroupGroup);
    leftPentagon.setAttribute("transform", `translate(0, ${fullPoint[1]})`);
    segmentVertices[segmentGroup[1]] = drawPentagon(leftPentagon, depth);

    const topLeftPentagon = drawGroup(segmentGroupGroup);
    topLeftPentagon.setAttribute(
      "transform",
      `translate(${subTriangleWidth / 2}, 0)`
    );
    segmentVertices[segmentGroup[2]] = drawPentagon(topLeftPentagon, depth);

    const topRightPentagon = drawGroup(segmentGroupGroup);
    topRightPentagon.setAttribute(
      "transform",
      `translate(${subTriangleWidth / 2 + subTriangleWidth + 2 * armWidth}, 0)`
    );
    segmentVertices[segmentGroup[3]] = drawPentagon(topRightPentagon, depth);

    const rightPentagon = drawGroup(segmentGroupGroup);
    rightPentagon.setAttribute(
      "transform",
      `translate(${subTriangleWidth + fullPoint[0]}, ${fullPoint[1]})`
    );
    segmentVertices[segmentGroup[4]] = drawPentagon(rightPentagon, depth);

    const centerPentagon = drawGroup(segmentGroupGroup);
    centerPentagon.setAttribute(
      "transform",
      `rotate(180 ${subTriangleWidth / 2} ${fullPoint[1] / 2})` +
        ` translate(-${subTriangleWidth + armWidth}, -${
          fullPoint[1] - headHeight
        })`
    );
    segmentVertices[segmentGroup[5]] = drawPentagon(centerPentagon, depth);
  });
};

const drawShape = {
  tetrahedron: drawTetrahedron,
  cube: drawCube,
  octahedron: drawOctahedron,
  dodecahedron: drawDodecahedron,
  icosahedron: drawIcosahedron,
};

export const shapeScales = {
  tetrahedron: [
    2 * CoordinateSystems.triangle.verticesPerSegmentPerRing * PATH_DISTANCE_60,
    2 * CoordinateSystems.triangle.verticesPerSegmentPerRing * UNIT_HEIGHT,
  ],
  cube: [
    4 * CoordinateSystems.square.verticesPerSegmentPerRing * UNIT_HEIGHT,
    3 * CoordinateSystems.square.verticesPerSegmentPerRing * UNIT_HEIGHT,
  ],
  octahedron: [
    4 * CoordinateSystems.triangle.verticesPerSegmentPerRing * PATH_DISTANCE_60,
    2 * CoordinateSystems.triangle.verticesPerSegmentPerRing * UNIT_HEIGHT,
  ],
  dodecahedron: [
    6 *
      CoordinateSystems.pentagon.verticesPerSegmentPerRing *
      PATH_DISTANCE_54 *
      3,
    3 *
      CoordinateSystems.pentagon.verticesPerSegmentPerRing *
      PATH_DISTANCE_54 *
      3,
  ],
  icosahedron: [
    5.5 *
      CoordinateSystems.triangle.verticesPerSegmentPerRing *
      PATH_DISTANCE_60,
    3 * CoordinateSystems.triangle.verticesPerSegmentPerRing * UNIT_HEIGHT,
  ],
};

export const faceWidths = {
  tetrahedron:
    CoordinateSystems.triangle.verticesPerSegmentPerRing * PATH_DISTANCE_60,
  cube: CoordinateSystems.square.verticesPerSegmentPerRing * UNIT_HEIGHT,
  octahedron:
    CoordinateSystems.triangle.verticesPerSegmentPerRing * PATH_DISTANCE_60,
  dodecahedron:
    CoordinateSystems.pentagon.verticesPerSegmentPerRing *
    PATH_DISTANCE_54 *
    (1 + 2 * COS72),
  icosahedron:
    CoordinateSystems.triangle.verticesPerSegmentPerRing * PATH_DISTANCE_60,
};

export default drawShape;
