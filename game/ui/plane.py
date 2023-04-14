import pygame
import moderngl
import glm
from engine.renderable import Renderable
import numpy as np

from engine.events.mouse import ClickDetector, find_mouse_face


SQUARE_VERTICES = np.array(
    [
        (-1 , -1 , 0),  # 0
        ( 1 , -1 , 0),  # 1
        (-1 ,  1 , 0),  # 2
        ( 1 ,  1 , 0),  # 3
    ],
    dtype="f4",
)
SQUARE_CLIP = [
  glm.vec4(SQUARE_VERTICES[0], 1.0),
  glm.vec4(SQUARE_VERTICES[1], 1.0),
  glm.vec4(SQUARE_VERTICES[3], 1.0),
  glm.vec4(SQUARE_VERTICES[2], 1.0),
]

class Plane(Renderable):
    def __init__(
        self,
        ctx: moderngl.Context,
        camera_matrix,
        position: glm.vec3,
        dimensions: glm.vec2 = glm.vec2(1.0, 1.0),
        **kwargs
    ):
        self.ctx = ctx

        self.matrix = (
            camera_matrix
            * glm.translate(position)
            * glm.scale(glm.vec3(dimensions.xy, 1.0))
        )

        self.vertex_data = self._get_vertex_data()
        self.click_vertices = [[self.matrix * v for v in SQUARE_CLIP]]

        self.obj = self._get_shadeable_object()
        self.obj.shader["m_mvp"].write(self.matrix)

        self.on_click = kwargs.get("on_click", None)
        self.click_detector = ClickDetector(on_click=self._on_click) if self.on_click else None

    def _get_shadeable_object(self):
        """
        override this to return a shadeable object of your choice
        """
        pass

    def _get_vertex_data(self):
        """
        override this to return vertices in your format
        """
        return SQUARE_VERTICES

    def _on_click(self, mouse_pos):
        if find_mouse_face(mouse_pos, self.click_vertices) == 0:
            self.on_click()

    def handle_event(self, event: pygame.event.Event, world_time: int):
        if self.click_detector:
            self.click_detector.handle_event(event, world_time)

    def render(self):
        self.obj.render(mode=moderngl.TRIANGLE_STRIP)

    def destroy(self):
        self.obj.destroy()
