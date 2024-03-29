from constants.shape import Shape
from constants.colors import Colors, ShapeStyle, BlendModes, set_opacity
from engine.audio.soundtrack import SoundtrackSong

LEVELS = [
    {
        "shape": Shape.tetrahedron,
        "puzzles": [
            "4_mouse",
            "4_diamonds",
            "4_ovals",
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
            "6_lanes",
            "6_sudoku",
            "6_giftbox",
            "6_box_corners",
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
            "8_para",
            "8_chevron",
            "8_beats",
            "8_symbols",
        ],
        "style": ShapeStyle(
            "wind09.png",
            Colors.CYAN,
            Colors.TEAL_GRAY,
            Colors.TEAL_GRAY,
            BlendModes.Reflect,
        ),
        "song": SoundtrackSong.wind,
    },
    {
        "shape": Shape.icosahedron,
        "puzzles": [
            "20_soccer",
            "20_stars",
            "20_swirls",
            "20_parallels",
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
            "12_sapphire",
            "12_mustaches",
            "12_easy",
            "12_zipper",
        ],
        "style": ShapeStyle(
            "aether03.png",
            Colors.MOON_DUST,
            Colors.MOON_SHAODW,
            Colors.MOON_SHAODW,
            BlendModes.Multipy,
        ),
        "song": SoundtrackSong.cosmos,
    },
]
