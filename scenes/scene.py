class Scene:
    def handle_events(self, delta_time: int):
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
