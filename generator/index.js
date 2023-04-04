import { UNIT_HEIGHT, SVG_PADDING } from "./constants.js";
import drawShape, { shapeScales, faceWidths } from "./drawShape.js";

const shapeEl = document.getElementById("shapeInput");
const depthEl = document.getElementById("depthInput");
const exportEl = document.getElementById("exportButton");

let faces = {};

let shape = shapeEl.value;
shapeEl.addEventListener("change", () => {
  shape = shapeEl.value;
  render();
});

let depth = parseInt(depthEl.value);
depthEl.addEventListener("change", () => {
  depth = parseInt(depthEl.value);
  render();
});

exportEl.addEventListener("click", () => {
  const dataPayload = {
    shape,
    depth,
    faces: [],
  };

  const faceWidth = faceWidths[shape] * depth;

  for (let faceKey in faces) {
    const faceRings = faces[faceKey];

    const simplifiedVertices = [];
    const simplifiedPolygons = new Map();

    faceRings.forEach((ringVertices) => {
      const usefulVertices = ringVertices.filter((vertex) =>
        vertex.polygons.find((polygon) => polygon.is_active)
      );

      usefulVertices.forEach((vertex) => {
        simplifiedVertices.push({
          indices: vertex.indices,
          coordinates: [
            vertex.coordinates[0] / faceWidth,
            vertex.coordinates[1] / faceWidth,
          ],
        });

        vertex.polygons
          .filter((polygon) => polygon.is_active)
          .forEach((polygon) => {
            const polygonKey = JSON.stringify(
              polygon.vertices.map((v) => v.indices)
            );
            if (!simplifiedPolygons.has(polygonKey)) {
              simplifiedPolygons.set(
                polygonKey,
                polygon.vertices.map((v) => v.indices)
              );
            }
          });
      });
    });

    dataPayload.faces.push({
      vertices: simplifiedVertices,
      polygons: Array.from(simplifiedPolygons.values()),
    });
  }
  var dataStr =
    "data:text/json;charset=utf-8," +
    encodeURIComponent(JSON.stringify(dataPayload));
  var downloadAnchorNode = document.createElement("a");
  downloadAnchorNode.setAttribute("href", dataStr);
  downloadAnchorNode.setAttribute(
    "download",
    `platonica-puzzle-${new Date().getTime()}.json`
  );
  document.body.appendChild(downloadAnchorNode); // required for firefox
  downloadAnchorNode.click();
  downloadAnchorNode.remove();
});

// Canvas
const svg = document.getElementById("svg");

const resetCanvas = () => {
  svg.innerHTML = "";
  const shapeScale = shapeScales[shape];
  svg.setAttribute("height", shapeScale[1] * depth + 2 * SVG_PADDING);
  svg.setAttribute("width", shapeScale[0] * depth + 2 * SVG_PADDING);
};

const render = () => {
  resetCanvas();
  faces = drawShape[shape](svg, depth);
};

render();
