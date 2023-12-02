from constants.shape import FaceShape, Shape
from engine.vectors import normalize_vector
import math
import numpy as np

RING_UNIT_Y = -1
RING_UNIT_X_SQUARE = RING_UNIT_Y
RING_UNIT_X_EQUILATERAL = 1.5 * RING_UNIT_Y / np.cos(np.radians(30))
RING_UNIT_X_PENTAGONAL = 1.0 * RING_UNIT_Y / np.tan(np.radians(54))
COS72 = np.cos(np.deg2rad(72))
class FaceGeneratorDefinition:
  @staticmethod
  def from_shape(shape: Shape):
    return shape_face_systems[shape]

  def __init__(
    self,
    num_segments: int,
    vertices_per_segment_per_ring: int,
    ring_vector: tuple[float, float],
    segment_rotation: int,
    segment_length: float,
  ):
    self.num_segments = num_segments
    self.vertices_per_segment_per_ring = vertices_per_segment_per_ring
    self.ring_vector = np.array(ring_vector, dtype='f4')
    self.segment_rotation = np.radians(segment_rotation)
    self.segment_length = segment_length

  def segment_for_vertex(self, ring_idx: int, count_idx: int):
    vertices_per_segment = self.vertices_per_segment_per_ring * ring_idx
    if vertices_per_segment == 0:
      return None
    return math.floor(count_idx / vertices_per_segment)

  def vertex_count_for_ring(self, ring_idx: int):
    if ring_idx == 0:
      return 1
    return self.vertices_per_segment_per_ring * self.num_segments * ring_idx

  def vertex_range_for_segment(self, segment_idx: int, ring_idx: int, extra=0):
    vertices_per_segment = self.vertices_per_segment_per_ring * ring_idx
    return range(
      vertices_per_segment * segment_idx,
      vertices_per_segment * (segment_idx+1) + extra,
    )

  def get_center_uv_coordinates(self, depth: int):
    origin = np.array([0,0], dtype='f4')
    return origin - (depth * self.ring_vector)

  def indices_to_uv_coordinates(self, indices: tuple[int, int], depth: int):
    (ring_idx, count_idx) = indices
    vertices_per_segment = self.vertices_per_segment_per_ring * ring_idx;
    center = self.get_center_uv_coordinates(depth)
    ring_origin = center + (self.ring_vector * ring_idx)
    point_segment = math.floor(
      count_idx / self.vertices_per_segment_per_ring * ring_idx
    )

    uv_coordinates = ring_origin.copy()
    for segment in range(point_segment+1):
      rotation_angle = self.segment_rotation * segment
      segment_vector = [
        np.cos(rotation_angle),
        np.sin(rotation_angle),
      ]
      segment_vertex_count = vertices_per_segment if segment != point_segment else count_idx % vertices_per_segment
      uv_coordinates = uv_coordinates * (segment_vertex_count * segment_vector)

    return normalize_vector(uv_coordinates, 1)

  def rotated_count_idx(self, ring_idx: int, count_idx: int, rotation_count: int):
    # Rotation shifts every vertex by -vertices_per_segment
    vertex_count = self.vertex_count_for_ring(ring_idx)
    vertices_per_segment = self.vertices_per_segment_per_ring * ring_idx
    shifted_count_idx = (count_idx - (rotation_count * vertices_per_segment))
    return (vertex_count + shifted_count_idx) % vertex_count

face_systems = {
  FaceShape.triangle: FaceGeneratorDefinition(
    num_segments=3,
    vertices_per_segment_per_ring=3,
    ring_vector=[RING_UNIT_X_EQUILATERAL, RING_UNIT_Y],
    segment_rotation=120,
    segment_length=1
  ),
  FaceShape.square: FaceGeneratorDefinition(
    num_segments=4,
    vertices_per_segment_per_ring=2,
    ring_vector=[RING_UNIT_X_SQUARE, RING_UNIT_Y],
    segment_rotation=90,
    segment_length=1
  ),
  FaceShape.pentagon: FaceGeneratorDefinition(
    num_segments=5,
    vertices_per_segment_per_ring=1,
    ring_vector=[RING_UNIT_X_PENTAGONAL, RING_UNIT_Y],
    segment_rotation=72,
    segment_length=(1 + (2 * COS72))
  ),
}

shape_face_systems = {
  Shape.tetrahedron: face_systems[FaceShape.triangle],
  Shape.cube: face_systems[FaceShape.square],
  Shape.octahedron: face_systems[FaceShape.triangle],
  Shape.dodecahedron: face_systems[FaceShape.pentagon],
  Shape.icosahedron: face_systems[FaceShape.triangle],
}
