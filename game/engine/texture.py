import os
import pygame
import moderngl

dir_path = os.path.dirname(os.path.realpath(__file__))

_next_texture_location = 0
texture_atlas = dict()


def get_texture(ctx: moderngl.Context, texture_filename: str):
    if texture_filename in texture_atlas:
        return texture_atlas[texture_filename]
    else:
        return _get_texture_by_filename(ctx, texture_filename)

def _get_texture_by_filename(ctx: moderngl.Context, texture_filename: str):
    global _next_texture_location
    path = os.path.join(dir_path, '..','assets','textures',texture_filename)
    texture_surface = pygame.image.load(path).convert()
    texture_surface = pygame.transform.flip(texture_surface, flip_x=False, flip_y=True)
    texture = ctx.texture(
        size=texture_surface.get_size(),
        components=4,
        data=pygame.image.tostring(texture_surface, 'RGBA')
    )
    texture_location = _next_texture_location
    texture.use(location=texture_location)
    texture_atlas[texture_filename] = (texture, texture_location)
    _next_texture_location = _next_texture_location + 1
    return (texture, texture_location)


texture_maps = {
    'tetra_debug.png': {
        'uv': [
            (0.504, 0.953), #0
            (0.262, 0.496), #1
            (0.744, 0.496), #2
            (0.02, 0.142), #3
            (0.504, 0.142), #4
            (0.986, 0.142), #5
        ],
        'faces': [
            (1, 0, 2),
            (1, 4, 3),
            (4, 1, 2),
            (2, 5, 4),
            (1, 0, 2),
            (1, 4, 3),
            (4, 1, 2),
        ]
    },
    'david-jorre-unsplash.png': {
        'uv': [
            (0.504, 0.953), #0
            (0.262, 0.496), #1
            (0.744, 0.496), #2
            (0.02, 0.142), #3
            (0.504, 0.142), #4
            (0.986, 0.142), #5
        ],
        'faces': [
            (1, 0, 2),
            (1, 4, 3),
            (4, 1, 2),
            (2, 5, 4),
        ]
    }
}