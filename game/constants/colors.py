import glm

class Colors:
    WHITE       = glm.vec4(1.0, 1.0, 1.0, 1.0)
    GRAY        = glm.vec4(0.5, 0.5, 0.5, 1.0)
    LIGHT_GRAY  = glm.vec4(0.8, 0.8, 0.8, 1.0)
    CHARCOAL    = glm.vec4(0.1, 0.1, 0.1, 1.0)
    GREEN       = glm.vec4(0.0, 1.0, 0.1, 1.0)
    LIME        = glm.vec4(0.25, .67, 0.15, 1.0)
    RED         = glm.vec4(1.0, 0, 0, 1.0)
    DARK_RED    = glm.vec4(0.95, 0.3, 0.2, 1.0)

class BlendModes:
    Opaque      = 0
    Overlay     = 1
    Multipy     = 2
    Reflect     = 3

def set_opacity(color: glm.vec4, opacity: float):
    return glm.vec4(color.rgb, opacity)