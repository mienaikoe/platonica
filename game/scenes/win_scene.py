import moderngl
from constants.colors import Colors
from engine.renderable import Renderable
from engine.camera import Camera
from engine.animation import Animator
from engine.animation import AnimationLerpFunction, AnimationLerper
from models.starfield import make_starfield
from engine.events import emit_event, LEVEL_LOADED, PUZZLE_LOADED
from engine.audio.soundtrack import SoundtrackSong
from models.planets import SolarSystem


INTRO_DURATION = 10000  # ms


class WinScene(Renderable):
    def __init__(self, ctx: moderngl.Context, camera: Camera):
        self.ctx = ctx
        self.camera = camera

        self.starfield = make_starfield(ctx)
        self.camera_animator = Animator(
            AnimationLerper(AnimationLerpFunction.ease_in_out, INTRO_DURATION), -12
        )

        self.planets = SolarSystem(ctx, camera)

    def init(self):
        emit_event(LEVEL_LOADED, {"song": SoundtrackSong.win})
        emit_event(PUZZLE_LOADED)
        self.camera_animator.start(-4.0)
        self.planets.start()

    # def handle_event(self, event: pygame.event.Event, world_time: int):
    #     self.subject.handle_event(event, world_time)

    def render(self, delta_time: int):
        self.ctx.clear(color=Colors.BLACK)
        if self.camera_animator.is_animating:
            self.camera.set_z(self.camera_animator.frame(delta_time))
        self.starfield.render(
            uniforms={"m_mvp": self.camera.view_projection_matrix},
            mode=moderngl.TRIANGLES,
        )
        self.starfield.render()
        self.planets.render(delta_time)

    # def destroy(self):
    #     self.subject.destroy()
