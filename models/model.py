import moderngl
import glm
import pygame
from constants.vectors import UnitVector

from engine.camera import Camera

MOVEMENT_DEG_PER_DELTA = 0.001


class Model:
    def __init__(self, ctx: moderngl.Context, camera: Camera):
        self.ctx = ctx
        self.camera = camera
        self.shader_program = self.get_shader_program("default")
        self.shader_program["m_proj"].write(camera.projection_matrix)
        self.shader_program["m_view"].write(camera.view_matrix)
        self.m_model = glm.mat4()
        self.vertex_buffer_object = self.get_vertex_buffer_object()
        self.vertex_array_object = self.get_vertex_array_object()

    def render(self, delta_time: int):
        self.shader_program["m_model"].write(self.m_model)
        self.vertex_array_object.render()

    def destroy(self):
        self.vertex_buffer_object.release()
        self.shader_program.release()
        self.vertex_array_object.release()

    def get_vertex_array_object(self):
        vertex_array_object = self.ctx.vertex_array(
            self.shader_program,
            [
                (self.vertex_buffer_object, "2f 3f", "in_textcoord_0", "in_position"),
            ],
        )
        return vertex_array_object

    def get_vertex_data(self):
        """
        return an np.array with dtype='f4' (4 byte float)
        that represents the vertices of your model
        """
        pass

    def get_vertex_buffer_object(self):
        vertex_data = self.get_vertex_data()
        vertex_buffer = self.ctx.buffer(vertex_data)
        return vertex_buffer

    def get_shader_program(self, shader_name):
        with open(f"engine/shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"engine/shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program

    def handle_events(self, delta_time: int):
        displacement = MOVEMENT_DEG_PER_DELTA * delta_time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.m_model = glm.rotate(self.m_model, displacement, UnitVector.RIGHT)
        if keys[pygame.K_s]:
            self.m_model = glm.rotate(self.m_model, -displacement, UnitVector.RIGHT)
        if keys[pygame.K_d]:
            self.m_model = glm.rotate(self.m_model, displacement, UnitVector.UP)
        if keys[pygame.K_a]:
            self.m_model = glm.rotate(self.m_model, -displacement, UnitVector.UP)
