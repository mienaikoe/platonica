from enum import Enum
import math

class AnimationLerpFunction(Enum):
  linear = 'linear'
  ease_out = 'ease_out'
  ease_in = 'ease_in'
  ease_in_out = 'ease_in_out'

class AnimationLerper:

  def __init__(
    self,
    function: AnimationLerpFunction,
    duration_ms: int,
    bounds: tuple[float, float]
  ):
    self.__set_function(function)
    self.duration_ms = duration_ms
    self.set_bounds(bounds)

  def __set_function(self, function: AnimationLerpFunction):
    match(function):
      case AnimationLerpFunction.linear:
        self._interpolator = self._interpolate_linear
      case AnimationLerpFunction.ease_out:
        self._interpolator = self._interpolate_ease_out
      case AnimationLerpFunction.ease_in:
        self._interpolator = self._interpolate_ease_in
      case AnimationLerpFunction.ease_in_out:
        self._interpolator = self._interpolate_ease_in_out

  def set_bounds(self, bounds: tuple[float, float]):
    self.bounds = bounds
    self.difference = bounds[1] - bounds[0]

  def _interpolate_ease_in(self, time_elapsed: float):
    animation_percent = math.pow(time_elapsed / self.duration_ms, 5)
    animation_difference = animation_percent * self.difference
    return self.bounds[0] + animation_difference

  def _interpolate_ease_out(self, time_elapsed: float):
    time_percent = time_elapsed / self.duration_ms
    animation_percent = 1 - math.pow(1-time_percent, 5)
    animation_difference = animation_percent * self.difference
    return self.bounds[0] + animation_difference

  def _interpolate_ease_in_out(self, time_elapsed: float):
    time_percent = time_elapsed / self.duration_ms
    out_val = self._interpolate_ease_out(time_elapsed)
    in_val = self._interpolate_ease_in(time_elapsed)
    return (in_val + (out_val - in_val) * time_percent)

  def _interpolate_linear(self, time_elapsed: float):
    animation_percent = (time_elapsed / self.duration_ms)
    animation_difference = animation_percent * self.difference
    return self.bounds[0] + animation_difference

  def interpolate(self, time_elapsed: float):
    if time_elapsed >= self.duration_ms:
      return self.bounds[1]
    elif time_elapsed == 0:
      return self.bounds[0]
    else:
      return self._interpolator(time_elapsed)