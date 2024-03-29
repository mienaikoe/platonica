import glm


class Colors:
    BLACK = glm.vec4(0.0,0.0,0.0,1.0)
    WHITE = glm.vec4(1.0, 1.0, 1.0, 1.0)
    GRAY = glm.vec4(0.5, 0.5, 0.5, 1.0)
    LIGHT_GRAY = glm.vec4(0.8, 0.8, 0.8, 1.0)
    CHARCOAL = glm.vec4(0.1, 0.1, 0.1, 1.0)
    GREEN = glm.vec4(0.0, 1.0, 0.1, 1.0)
    LIME = glm.vec4(0.25, 0.67, 0.15, 1.0)
    APPLE_GREEN = glm.vec4(0.285, 0.898, 0.305, 1.0)
    RED = glm.vec4(1.0, 0, 0, 1.0)
    DARK_RED = glm.vec4(0.95, 0.3, 0.2, 1.0)
    PALE_BLUE = glm.vec4(0.5, 0.7, 1.0, 1.0)
    ROBIN_EGG = glm.vec4(0.1015, 0.6171, 0.7265, 1.0)
    STEEL_GRAY = glm.vec4(0.3764, 0.5176, 0.6, 1.0)
    POTATO = glm.vec4(0.2666, 0.2117, 0.1725, 1.0)
    COCOA = glm.vec4(0.1601, 0.1328, 0.1054, 1.0)
    CYAN = glm.vec4(0.157, 0.812, 1.0, 1.0)
    SKY_BLUE = glm.vec4(0.518, 0.894, 1.0, 1.0)
    TEAL_GRAY = glm.vec4(0.286, 0.325, 0.318, 1.0)
    MOON_SHAODW = glm.vec4(0.447, 0.427, 0.471, 1.0)
    MOON_DUST = glm.vec4(0.745, 0.62, 1.0, 1.0)


class BlendModes:
    Opaque = 0
    Overlay = 1
    Multipy = 2
    Reflect = 3
    Screen = 4
    ColorBurn = 5


def set_opacity(color: glm.vec4, opacity: float):
    return glm.vec4(color.rgb, opacity)


class ShapeStyle:
    def __init__(
        self,
        texture_name: str,
        path_color: glm.vec4,
        wall_color: glm.vec4,
        underside_color: glm.vec4,
        blend_mode: BlendModes,
    ):
        self.texture_name = texture_name
        self.path_color = path_color
        self.wall_color = wall_color
        self.underside_color = underside_color
        self.blend_mode = blend_mode
