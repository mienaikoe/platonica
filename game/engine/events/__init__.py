import pygame

FACE_ACTIVATED = pygame.USEREVENT + 1

def emit_face_activated(face_index):
    evt = pygame.event.Event(FACE_ACTIVATED, { 'face_index': face_index })
    pygame.event.post(evt)