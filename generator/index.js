import { UNIT_HEIGHT, UNIT_WIDTH, SVG_PADDING } from "./constants.js";
import drawShape from "./drawShape.js";

const shapeEl = document.getElementById("shapeInput");
const depthEl = document.getElementById("depthInput");
const exportEl = document.getElementById("exportButton");

let segmentVertices = {};

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
    depth,
    segments: {},
  };
  for (let key in segmentVertices) {
    const redVertices = segmentVertices[key];
    const simplifiedVertices = redVertices.map((greenVertices) => {
      return greenVertices.map((vertex) => {
        return {
          ...vertex,
          coordinates: [
            vertex.coordinates[0] / UNIT_WIDTH,
            vertex.coordinates[1] / UNIT_WIDTH,
          ],
          paths: vertex.paths.filter((path) => path.active),
        };
      });
    });

    dataPayload.segments[key] = simplifiedVertices;
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
  const segmentHeight = UNIT_HEIGHT * (depth - 1);
  const segmentWidth = UNIT_WIDTH * (depth - 1);
  svg.setAttribute("height", 2 * segmentHeight + 2 * SVG_PADDING);
  svg.setAttribute("width", 2 * segmentWidth + 2 * SVG_PADDING);
};

const render = () => {
  resetCanvas();
  segmentVertices = drawShape[shape](svg, depth);
};

render();
