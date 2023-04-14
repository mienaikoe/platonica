from constants.shape import Shape
from constants.colors import Colors, ShapeStyle, BlendModes, set_opacity

LEVELS = [
  {
    "shape": Shape.tetrahedron,
    "puzzles": [
      "4_4",
      "4_5a",
      "4_6a",
      "4_alien",
    ],
    "style": ShapeStyle(
        "david-jorre-unsplash_lighter.png",
        Colors.RED,
        Colors.CHARCOAL,
        Colors.CHARCOAL,
        BlendModes.Overlay
    ),
  },{
    "shape": Shape.cube,
    "puzzles": [
      "6_sudoku",
    ],
    "style": ShapeStyle(
      "cube06a.png",
      Colors.APPLE_GREEN,
      Colors.CHARCOAL,
      Colors.CHARCOAL,
      BlendModes.Reflect
    ),
  }, {
    "shape": Shape.octahedron,
    "puzzles": [
      "8_Xs_and_Os",
    ],
    "style": ShapeStyle(
      "david-jorre-unsplash_lighter.png",
      Colors.GRAY,
      Colors.CHARCOAL,
      Colors.CHARCOAL,
      BlendModes.Opaque
    ),
  }, {
    "shape": Shape.icosahedron,
    "puzzles": [
      "20_stars",
    ],
    "style":  ShapeStyle(
      "david-jorre-unsplash_lighter.png",
      Colors.GRAY,
      Colors.CHARCOAL,
      Colors.CHARCOAL,
      BlendModes.Opaque
    ),
  },
]