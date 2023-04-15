import glm

class Colors:
    WHITE       = glm.vec4(1.0, 1.0, 1.0, 1.0)
    GRAY        = glm.vec4(0.5, 0.5, 0.5, 1.0)
    LIGHT_GRAY  = glm.vec4(0.8, 0.8, 0.8, 1.0)
    CHARCOAL    = glm.vec4(0.1, 0.1, 0.1, 1.0)
    GREEN       = glm.vec4(0.0, 1.0, 0.1, 1.0)
    LIME        = glm.vec4(0.25, .67, 0.15, 1.0)
    APPLE_GREEN = glm.vec4(0.285, 0.898, 0.305, 1.0)
    RED         = glm.vec4(1.0, 0, 0, 1.0)
    DARK_RED    = glm.vec4(0.95, 0.3, 0.2, 1.0)
    PALE_BLUE   = glm.vec4(0.5, 0.7, 1.0, 1.0)

class BlendModes:
    Opaque      = 0
    Overlay     = 1
    Multipy     = 2
    Reflect     = 3
    Screen      = 4

def set_opacity(color: glm.vec4, opacity: float):
    return glm.vec4(color.rgb, opacity)

class ShapeStyle:
  def __init__(
    self,
    texture_name: str,
    path_color: glm.vec4,
    wall_color: glm.vec4,
    underside_color: glm.vec4,
    blend_mode: BlendModes
  ):
    self.texture_name = texture_name
    self.path_color = path_color
    self.wall_color = wall_color
    self.underside_color = underside_color
    self.blend_mode = blend_mode

