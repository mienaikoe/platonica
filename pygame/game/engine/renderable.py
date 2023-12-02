import pygame

class Renderable:
    def handle_event(self, event: pygame.event.Event, world_time: int):
        """
        handle any incoming events before the render
        @param delta_time: the number of milliseconds(?) since the last frame
        """
        pass

    def render(self, delta_time: int):
        """
        Render objects to the context.
        @param delta_time: the number of milliseconds(?) since the last frame
        """
        pass

    def init(self):
        """
        Initialize things, load textures into memory, etc
        """
        pass

    def destroy(self):
        """
        Remove any gl objects, as they are not garbage collected
        """
        pass
