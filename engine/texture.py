import pygame
import moderngl

def get_texture(ctx: moderngl.Context, path: str):
    texture = pygame.image.load(path).convert()
    texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
    texture = ctx.texture(
        size=texture.get_size(),
        components=3,
        data=pygame.image.tostring(texture, 'RGB'))
    return texture

texture_maps = {
    'tetra_tex_test.png': {
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