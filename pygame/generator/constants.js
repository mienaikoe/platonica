export const DEG_TO_RAD = Math.PI / 180;

// for triangle-red coordinate system
export const COS30 = Math.cos(30 * DEG_TO_RAD);
export const COS45 = Math.cos(45 * DEG_TO_RAD);
export const TAN30 = Math.tan(30 * DEG_TO_RAD);
export const SIN60 = Math.sin(60 * DEG_TO_RAD);
export const COS72 = Math.cos(72 * DEG_TO_RAD);
export const SIN72 = Math.sin(72 * DEG_TO_RAD);
export const TAN72 = Math.tan(72 * DEG_TO_RAD);
export const SIN54 = Math.sin(54 * DEG_TO_RAD);
export const COS54 = Math.cos(54 * DEG_TO_RAD);
export const TAN54 = Math.tan(54 * DEG_TO_RAD);
export const COS36 = Math.cos(36 * DEG_TO_RAD);
export const SIN36 = Math.sin(36 * DEG_TO_RAD);

// UNIT is 1 equilateral triangle
export const UNIT_HEIGHT = 40; // distance between rings at parallels
export const PATH_DISTANCE_60 = UNIT_HEIGHT / COS30; // path distance between nodes in the same ring
export const PATH_DISTANCE_45 = UNIT_HEIGHT / COS45;
export const PATH_DISTANCE_54 = (2 * UNIT_HEIGHT) / TAN54;

export const SVG_PADDING = 20;

export const CoordinateSystems = {
  triangle: {
    numSegments: 3,
    verticesPerSegmentPerRing: 3,
    ringShiftUnit: [-(1.5 * PATH_DISTANCE_60), -UNIT_HEIGHT],
    segmentUnitVectors: [
      [PATH_DISTANCE_60, 0],
      [-PATH_DISTANCE_60 / 2, UNIT_HEIGHT],
      [-PATH_DISTANCE_60 / 2, -UNIT_HEIGHT],
    ],
    verticesPerCorner: 3,
  },
  square: {
    numSegments: 4,
    verticesPerSegmentPerRing: 2,
    ringShiftUnit: [-UNIT_HEIGHT, -UNIT_HEIGHT],
    segmentUnitVectors: [
      [UNIT_HEIGHT, 0],
      [0, UNIT_HEIGHT],
      [-UNIT_HEIGHT, 0],
      [0, -UNIT_HEIGHT],
    ],
    verticesPerCorner: 1,
  },
  pentagon: {
    numSegments: 5,
    verticesPerSegmentPerRing: 1,
    ringShiftUnit: [-(PATH_DISTANCE_54 / 2), -UNIT_HEIGHT],
    segmentUnitVectors: [
      [PATH_DISTANCE_54, 0],
      [PATH_DISTANCE_54 * COS72, PATH_DISTANCE_54 * SIN72],
      [-PATH_DISTANCE_54 * COS36, PATH_DISTANCE_54 * SIN36],
      [-PATH_DISTANCE_54 * COS36, -PATH_DISTANCE_54 * SIN36],
      [PATH_DISTANCE_54 * COS72, -PATH_DISTANCE_54 * SIN72],
    ],
    verticesPerCorner: 1,
  },
};
