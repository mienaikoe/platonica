import { UNIT_HEIGHT, UNIT_WIDTH, SVG_PADDING } from "./constants.js";
import { drawGroup } from "./drawSvg.js";
import { drawTriangle } from "./drawFace.js";

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
