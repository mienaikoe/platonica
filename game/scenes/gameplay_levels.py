from constants.shape import Shape
from constants.colors import Colors, ShapeStyle, BlendModes, set_opacity
from engine.audio.soundtrack import SoundtrackSong

LEVELS = [
  {
      "shape": Shape.tetrahedron,
      "puzzles": [
          "4_4",
          # "4_5a",
          # "4_6a",
          "4_alien",
      ],
      "style": ShapeStyle(
          "david-jorre-unsplash_lighter.png",
          Colors.RED,
          Colors.CHARCOAL,
          Colors.CHARCOAL,
          BlendModes.Overlay,
      ),
      "song": SoundtrackSong.fire,
  },
  {
      "shape": Shape.cube,
      "puzzles": [
          "6_sudoku",
      ],
      "style": ShapeStyle(
          "cube06a.png",
          Colors.APPLE_GREEN,
          Colors.COCOA,
          Colors.COCOA,
          BlendModes.Reflect,
      ),
      "song": SoundtrackSong.earth,
  },
  {
      "shape": Shape.octahedron,
      "puzzles": [
          "8_chevron",
      ],
      "style": ShapeStyle(
          "david-jorre-unsplash_lighter.png",
          Colors.WHITE,
          Colors.CHARCOAL,
          Colors.CHARCOAL,
          BlendModes.Opaque,
      ),
      "song": SoundtrackSong.wind,
  },
  {
      "shape": Shape.icosahedron,
      "puzzles": [
          "20_stars",
      ],
      "style": ShapeStyle(
          "water_02.jpeg",
          Colors.ROBIN_EGG,
          Colors.STEEL_GRAY,
          Colors.STEEL_GRAY,
          BlendModes.ColorBurn,
      ),
      "song": SoundtrackSong.water,
  },
  {
      "shape": Shape.dodecahedron,
      "puzzles": [
          "12_pointy",
      ],
      "style": ShapeStyle(
          "ice-opaque.png",
          Colors.GRAY,
          Colors.CHARCOAL,
          Colors.CHARCOAL,
          BlendModes.Opaque,
      ),
      "song": SoundtrackSong.water,
  },
]
