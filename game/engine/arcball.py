"""
=======
ARCBALL
=======
Original C++ implementation
https://github.com/gamedev-net/nehe-opengl/blob/master/vc/Lesson48/ArcBall.h
https://github.com/gamedev-net/nehe-opengl/blob/master/vc/Lesson48/ArcBall.cpp
by Terence J. Grant
Date: Sept 25][2003
MIT License Copyright (c) 1997-2017 GameDev.net, LLC
Converted to python by Zishun Liu <liuzishun@gmail.com>
Date: Feb 21][2021

Copied from https://github.com/zishun/pyqt-meshviewer/blob/master/ArcBall.py
"""

import pygame
import numpy as np

from constants.dimensions import SCREEN_DIMENSIONS
__all__ = ['ArcBall', 'ArcBallUtil']

SQRT3 = np.sqrt(3)

class ArcBall:
    def __init__(self, on_transform_change: callable):
        # Saved Vectors - used so we don't allocate new vectors
        # every time an event occurs
        self.start_vector = np.zeros(3, 'f4')  # Saved click vector
        self.drag_vector = np.zeros(3, 'f4')  # Saved drag vector
        self.temp_coordinates = [None, None]

        # Adjustments for transforming mouse coordinates from pixel to cartesian space
        self.adjust_width = 1.0 / ((SCREEN_DIMENSIONS[0] - 1.0) * 0.5)
        self.adjust_height = 1.0 / ((SCREEN_DIMENSIONS[1] - 1.0) * 0.5)

        # assuming IEEE-754(GLfloat), which i believe has
        # max precision of 7 bits
        self.epsilon = 1.0e-5

        # the transforms for m_model
        self._rot3x3 = np.identity(3, dtype='f4')
        self._last_rot3x3 = np.identity(3, dtype='f4')
        self.transform = np.identity(4, dtype='f4')

        self.on_transform_change = on_transform_change

        self.is_dragging = False

    def handle_event(self, event: pygame.event.Event):
        match event.type:
          case pygame.MOUSEBUTTONDOWN:
              self.on_down(pygame.mouse.get_pos())
          case pygame.MOUSEBUTTONUP:
              self.on_up()
          case pygame.MOUSEMOTION:
              self.on_move(pygame.mouse.get_pos())

    def on_down(self, click_coordinates: tuple[int, int]):  # Mouse down
        self.is_dragging = True
        self._last_rot3x3 = self._rot3x3
        # Map the point to the sphere
        self._map_to_sphere(click_coordinates, self.start_vector)

    def on_move(self, drag_coordinates: tuple[int, int]):  # Mouse drag, calculate rotation
        if not self.is_dragging:
            return

        # Map the point to the sphere
        self._map_to_sphere(drag_coordinates, self.drag_vector)

        # Return the quaternion equivalent to the rotation
        # Compute the vector perpendicular to the begin and end vectors
        perpindicular = np.cross(self.start_vector, self.drag_vector)

        new_rotation_quat = np.zeros((4,), 'f4')

        # Compute the length of the perpendicular vector
        if np.linalg.norm(perpindicular) > self.epsilon:  # if its non-zero
            # We're ok, so return the perpendicular vector as the transform
            # after all
            new_rotation_quat[:3] = perpindicular[:3]
            # In the quaternion values, w is cosine (theta / 2), where theta
            # is rotation angle
            new_rotation_quat[3] = np.dot(self.start_vector, self.drag_vector)
        else:  # if its zero
            # The begin and end vectors coincide, so return an identity
            # transform
            pass

        # Convert Quaternion Into Matrix3fT
        self._rot3x3 = self.Matrix3fSetRotationFromQuat4f(new_rotation_quat)
        # Accumulate Last Rotation Into This One
        self._rot3x3 = np.matmul(self._last_rot3x3, self._rot3x3)
        # Set Our Final Transform's Rotation From This One
        self.transform = self.Matrix4fSetRotationFromMatrix3f(
            self.transform, self._rot3x3
        )
        # print(self.Transform)  # for debugging
        self.on_transform_change(self.transform)

    def on_up(self):
        if not self.is_dragging:
            return
        self.is_dragging = False
        self._last_rot3x3 = self._rot3x3

    # def reset(self):
        # self._last_rot3x3 = np.identity(3, 'f4')
        # self._rot3x3 = np.identity(3, 'f4')
        # self.transform = self.Matrix4fSetRotationFromMatrix3f(
        #   self.transform, self._rot3x3
        # )

    def _map_to_sphere(self, event_coordinates: tuple[int, int], update_vector):
        # Adjust point coords and scale down to range of [-1 ... 1]
        self.temp_coordinates[0] = (event_coordinates[0] * self.adjust_width) - 1.0
        self.temp_coordinates[1] = 1.0 - (event_coordinates[1] * self.adjust_height)

        # Compute the square of the length of the vector to the point from the
        # center
        length_squared = np.dot(self.temp_coordinates, self.temp_coordinates)

        # If the point is mapped outside of the sphere...
        # (length^2 > radius squared)
        if length_squared > 1.0:
            # Compute a normalizing factor (radius / sqrt(length))
            norm = 1.0 / np.sqrt(length_squared)

            # Return the "normalized" vector, a point on the sphere
            update_vector[0] = self.temp_coordinates[0] * norm
            update_vector[1] = -self.temp_coordinates[1] * norm
            update_vector[2] = 0.0
        else:    # Else it's on the inside
            # Return a vector to a point mapped inside the sphere
            # sqrt(radius squared - length^2)
            update_vector[0] = self.temp_coordinates[0]
            update_vector[1] = -self.temp_coordinates[1]
            update_vector[2] = np.sqrt(1.0 - length_squared)

    # Sets the rotational component (top-left 3x3) of NewObj to the matrix
    # values in the m3x3 argument; the other elements of NewObj are unchanged
    # a singular value decomposition is performed on NewObj's upper 3x3 matrix
    # to factor out the scale, then NewObj's upper 3x3 matrix components are
    # replaced by the passed rotation components m3x3, and then the scale is
    # reapplied to the rotational components.
    def Matrix4fSetRotationFromMatrix3f(self, rot_mat, m3x3):
        scale = np.linalg.norm(rot_mat[:3, :3], ord='fro') / SQRT3
        # rot_mat[0:3][0:3] = m3x3 * scale
        scaled_matrix = m3x3 * scale
        for x in range(3):
          for y in range(3):
            rot_mat[x][y] = scaled_matrix[x][y]
        return rot_mat

    def Matrix3fSetRotationFromQuat4f(self, quat):
        if np.sum(np.dot(quat, quat)) < self.epsilon:
            return np.identity(3, 'f4')

        # Copied from https://github.com/scipy/scipy/blob/main/scipy/spatial/transform/_rotation.pyx
        r = np.ndarray(shape=(3,3), dtype='f4')

        x = quat[0]
        y = quat[1]
        z = quat[2]
        w = quat[3]

        x2 = x * x
        y2 = y * y
        z2 = z * z
        w2 = w * w

        xy = x * y
        zw = z * w
        xz = x * z
        yw = y * w
        yz = y * z
        xw = x * w

        r[0][0] = x2 - y2 - z2 + w2
        r[1][0] = 2 * (xy + zw)
        r[2][0] = 2 * (xz - yw)

        r[0][1] = 2 * (xy - zw)
        r[1][1] = - x2 + y2 - z2 + w2
        r[2][1] = 2 * (yz + xw)

        r[0][2] = 2 * (xz + yw)
        r[1][2] = 2 * (yz - xw)
        r[2][2] = - x2 - y2 + z2 + w2

        return np.transpose(r)