import {
  UNIT_HEIGHT,
  UNIT_WIDTH_60,
  SVG_PADDING,
  UNIT_WIDTH_72,
  UNIT_WIDTH_54,
} from "./constants.js";
import { drawGroup } from "./drawSvg.js";
import { drawPentagon, drawSquare, drawTriangle } from "./drawFace.js";

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

  const fullPoint = [UNIT_WIDTH_60 * (depth - 1), UNIT_HEIGHT * (depth - 1)];
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

const drawCube = (svg, depth) => {
  const midpoint = [
    svg.getAttribute("width") / 2,
    svg.getAttribute("height") / 2,
  ];

  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(-${SVG_PADDING}, -${SVG_PADDING}) rotate(180, ${midpoint[0]}, ${midpoint[1]})`
  );

  const fullPoint = UNIT_HEIGHT * (depth - 1);
  const segmentTranslations = {
    A: [0, 1],
    B: [1, 0],
    C: [1, 1],
    D: [1, 2],
    E: [2, 1],
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
  const midpoint = [
    svg.getAttribute("width") / 2,
    svg.getAttribute("height") / 2,
  ];

  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(-${SVG_PADDING}, -${SVG_PADDING}) rotate(180, ${midpoint[0]}, ${midpoint[1]})`
  );

  const fullPoint = [UNIT_WIDTH_60 * (depth - 1), UNIT_HEIGHT * (depth - 1)];
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

  const fullPoint = [UNIT_WIDTH_60 * (depth - 1), UNIT_HEIGHT * (depth - 1)];
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
  const midpoint = [
    svg.getAttribute("width") / 2,
    svg.getAttribute("height") / 2,
  ];

  const containerGroup = drawGroup(svg);
  containerGroup.setAttribute(
    "transform",
    `translate(-${SVG_PADDING}, -${SVG_PADDING})`
  );

  const fullPoint = [UNIT_WIDTH_60 * (depth - 1), UNIT_HEIGHT * (depth - 1)];
  const segmentVertices = {};

  const segmentGroups = [
    ["A", "B", "C", "D", "E", "F"],
    ["G", "H", "I", "J", "K", "L"],
  ];

  segmentGroups.forEach((segmentGroup, ix) => {
    const bottomLeftPentagon = drawGroup(containerGroup);
    segmentVertices[segmentGroup[0]] = drawPentagon(bottomLeftPentagon, depth);
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
  tetrahedron: [2 * UNIT_WIDTH_60, 2 * UNIT_HEIGHT],
  cube: [3 * UNIT_HEIGHT, 3 * UNIT_HEIGHT],
  octahedron: [4 * UNIT_WIDTH_60, 2 * UNIT_HEIGHT],
  dodecahedron: [6 * UNIT_WIDTH_54 * 3, 3 * UNIT_WIDTH_54 * 3],
  icosahedron: [5.5 * UNIT_WIDTH_60, 3 * UNIT_HEIGHT],
};

export default drawShape;
