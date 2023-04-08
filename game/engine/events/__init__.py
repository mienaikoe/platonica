import pygame

FACE_ACTIVATED = pygame.USEREVENT + 1
FACE_ROTATING = pygame.USEREVENT + 2
FACE_ROTATED = pygame.USEREVENT + 3

LEVEL_WON = pygame.USEREVENT + 4

def emit_event(event_type: int, payload: any):
    evt = pygame.event.Event(event_type, payload)
    pygame.event.post(evt)

def emit_face_activated(face_index):
    emit_event(FACE_ACTIVATED, { 'face_index': face_index })

