import pygame

FACE_ACTIVATED = pygame.USEREVENT + 1
FACE_ROTATING = pygame.USEREVENT + 2
FACE_ROTATED = pygame.USEREVENT + 3

PUZZLE_SOLVED = pygame.USEREVENT + 5
DONE_RESONATE = pygame.USEREVENT + 6
NEXT_PUZZLE = pygame.USEREVENT + 7
NEXT_LEVEL = pygame.USEREVENT + 8
PUZZLE_LOADED = pygame.USEREVENT + 9
LEVEL_LOADED = pygame.USEREVENT + 10
PUZZLE_EXITED = pygame.USEREVENT + 11

ARCBALL_MOVE = pygame.USEREVENT + 15
ARCBALL_DONE = pygame.USEREVENT + 16

SCENE_FINISH = pygame.USEREVENT + 20

FADE_IN = pygame.USEREVENT + 25
FADED_IN = pygame.USEREVENT + 26
FADE_OUT = pygame.USEREVENT + 27
FADED_OUT = pygame.USEREVENT + 28

MUSIC_TRACK_END = pygame.USEREVENT + 30


def emit_event(event_type: int, payload: any = {}):
    evt = pygame.event.Event(event_type, payload)
    pygame.event.post(evt)

def block_events(type = None):
    pygame.event.set_blocked(type)
    print('block events')

def allow_events(type = None):
    pygame.event.set_allowed(type)
    print('allow events')