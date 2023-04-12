import pygame

FACE_ACTIVATED = pygame.USEREVENT + 1
FACE_ROTATING = pygame.USEREVENT + 2
FACE_ROTATED = pygame.USEREVENT + 3

PUZZLE_SOLVED = pygame.USEREVENT + 4
DONE_RESONATE = pygame.USEREVENT + 5
NEXT_PUZZLE = pygame.USEREVENT + 6

ARCBALL_MOVE = pygame.USEREVENT + 7

SCENE_FINISH = pygame.USEREVENT + 8

def emit_event(event_type: int, payload: any):
    evt = pygame.event.Event(event_type, payload)
    pygame.event.post(evt)

def emit_face_activated(face_index):
    emit_event(FACE_ACTIVATED, { 'face_index': face_index })

def block_events(type = None):
    pygame.event.set_blocked(type)
    print('block events')

def allow_events(type = None):
    pygame.event.set_allowed(type)
    print('allow events')