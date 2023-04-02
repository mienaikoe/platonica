from constants.shape import FaceShape, Shape
import math

class FaceGeneratorDefinition:
  @staticmethod
  def from_shape(shape: Shape):
    return shape_face_systems[shape]

  def __init__(self, num_segments: int, vertices_per_segment_per_ring: int):
    self.num_segments = num_segments
    self.vertices_per_segment_per_ring = vertices_per_segment_per_ring

  def segment_for_vertex(self, ring_idx: int, count_idx: int):
    vertices_per_segment = self.vertices_per_segment_per_ring * ring_idx
    if vertices_per_segment == 0:
      return None
    return math.floor(count_idx / vertices_per_segment)

  def vertex_count_for_ring(self, ring_idx: int):
    if ring_idx == 0:
      return 1
    return self.vertices_per_segment_per_ring * self.num_segments * ring_idx

  def vertex_range_for_segment(self, segment_idx: int, ring_idx: int):
    vertices_per_segment = self.vertices_per_segment_per_ring * ring_idx
    return range(
      vertices_per_segment * segment_idx,
      vertices_per_segment * (segment_idx+1) - 1,
    )

face_systems = {
  FaceShape.triangle: FaceGeneratorDefinition(3,3),
  FaceShape.square: FaceGeneratorDefinition(4,2),
  FaceShape.pentagon: FaceGeneratorDefinition(5,1),
}

shape_face_systems = {
  Shape.tetrahedron: face_systems[FaceShape.triangle],
  Shape.cube: face_systems[FaceShape.square],
  Shape.octahedron: face_systems[FaceShape.triangle],
  Shape.dodecahedron: face_systems[FaceShape.pentagon],
  Shape.icosahedron: face_systems[FaceShape.triangle],
}
