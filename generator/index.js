import drawShape from "./drawShape.js";

const shapeEl = document.getElementById("shape");
const depthEl = document.getElementById("depth");

let shape = shapeEl.value;
shapeEl.addEventListener("change", () => {
  shape = shapeEl.value;
  render();
});

let depth = depthEl.value;
depthEl.addEventListener("change", () => {
  depth = depthEl.value;
  render();
});

// Canvas
const svg = document.getElementById("svg");

const resetCanvas = () => {
  svg.innerHTML = "";
};

const render = () => {
  resetCanvas();
  drawShape[shape](svg, depth);
};

render();
