export const DEG_TO_RAD = Math.PI / 180;

// for triangle-red coordinate system
export const TAN30 = Math.tan(30 * DEG_TO_RAD);
export const SIN60 = Math.sin(60 * DEG_TO_RAD);
export const SIN72 = Math.sin(72 * DEG_TO_RAD);
export const SIN54 = Math.sin(54 * DEG_TO_RAD);
export const TAN54 = Math.tan(54 * DEG_TO_RAD);

// UNIT is 1 equilateral triangle
export const UNIT_HEIGHT = 40; // distance between two gridlines
export const UNIT_WIDTH_60 = UNIT_HEIGHT / SIN60; // distance between two vertices
export const UNIT_WIDTH_72 = UNIT_HEIGHT / SIN72;
export const UNIT_WIDTH_54 = UNIT_HEIGHT / SIN54;

export const SVG_PADDING = 20;
