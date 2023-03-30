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