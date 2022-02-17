
from enum import Enum
from typing import Tuple
from .chart3dhelp import *
from datetime import datetime

import numpy as np

def __append(_triangles, n1, n2, n3):
    f1 = np.array([[n1, n2, n3]])
    _triangles = np.append(_triangles, f1, axis=0)
    return _triangles


def __get_triangles(matrix: np.ndarray) -> np.ndarray:
    __triangles = np.empty((0, 3)).astype(np.int32)
    ad = np.shape(matrix)[1] * 4
    for xr in range(np.shape(matrix)[0]):
        xx = xr * ad
        af = (np.shape(matrix)[1] - 1) * 4 + xx
        if xr == 0:
            ab = 0
            ac = 0
        else:
            ab = ad - 3
            ac = ad - 2
        # links
        __triangles = __append(__triangles, 2 + xx, 1 + xx, 0 + xx)
        __triangles = __append(__triangles, 3 + xx, 1 + xx, 2 + xx)
        if xr != 0:
            __triangles = __append(__triangles, 2 + xx - ad, 0 + xx, 1 + xx)
            __triangles = __append(__triangles, 3 + xx - ad, 2 + xx - ad, 1 + xx)
        for fx in range(np.shape(matrix)[1] - 1):
            ae = fx * 4 + xx
            # vorne
            __triangles = __append(__triangles, 0 + ae - ab, 1 + ae, 4 + ae - ab)
            __triangles = __append(__triangles, 4 + ae - ab, 1 + ae, 5 + ae)
            # oben
            __triangles = __append(__triangles, 1 + ae, 3 + ae, 5 + ae)
            __triangles = __append(__triangles, 5 + ae, 3 + ae, 7 + ae)
            # unten
            __triangles = __append(__triangles, 4 + ae - ac, 2 + ae, 0 + ae - ac)
            __triangles = __append(__triangles, 6 + ae, 2 + ae, 4 + ae - ac)
            # rechts
        __triangles = __append(__triangles, 0 + af, 1 + af, 2 + af)
        __triangles = __append(__triangles, 2 + af, 1 + af, 3 + af)
        if xr != 0:
            __triangles = __append(__triangles, 2 + af - ad, 1 + af, 0 + af)
            __triangles = __append(__triangles, 2 + af - ad, 3 + af - ad, 1 + af)
    xx = np.shape(matrix)[1] * (np.shape(matrix)[0] - 1) * 4
    for fxx in range(np.shape(matrix)[1] - 1):
        __triangles = __append(__triangles, 6 + fxx * 4 + xx, 3 + fxx * 4 + xx, 2 + fxx * 4 + xx)
        __triangles = __append(__triangles, 7 + fxx * 4 + xx, 3 + fxx * 4 + xx, 6 + fxx * 4 + xx)
    return __triangles


def __append_quader(__vertices: np.ndarray,
                    __vcolors: np.ndarray,
                    __triangles: np.ndarray,
                    _vertices: np.ndarray,
                    _vcolors: np.ndarray,
                    _triangles: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if __vertices is None:
        __vertices = np.array(_vertices)
        __vcolors = np.array(_vcolors)
        __triangles = np.array(_triangles)
    else:
        dd = np.shape(__vertices)[0]
        __vertices = np.append(__vertices, _vertices, axis=0)
        __vcolors = np.append(__vcolors, _vcolors, axis=0)
        _triangles = _triangles + np.array([dd, dd, dd])
        __triangles = np.append(__triangles, _triangles, axis=0)

    return __vertices, __vcolors, __triangles


def __get_quader(z: float = 1,
                 colx: Color = Color(0, 1.0, 0.0),
                 dxyz: Point = Point(0, 0, 0),
                 zoom: Point = Point(1, 1, 1),
                 sockel: float =-1
                 ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    __vertices = np.empty((0, 3)).astype(np.float64)
    __vcolors = np.empty((0, 3)).astype(np.float64)
    __triangles = np.empty((0, 3)).astype(np.int32)

    vert = np.array([[0, 0, sockel], [1, 0, sockel], [1, 1, sockel], [0, 1, sockel]], dtype=float)
    __vertices = np.append(__vertices, vert, axis=0)
    vert2 = np.array([[0, 0, z], [1, 0, z], [1, 1, z], [0, 1, z]], dtype=float)
    __vertices = np.append(__vertices, vert2, axis=0)
    __vertices = __vertices + dxyz.get_array()
    __vertices = __vertices * zoom.get_array()
    col = np.array([colx.get_array(), colx.get_array(), colx.get_array(), colx.get_array()], dtype=float)
    __vcolors = np.append(__vcolors, col, axis=0)
    col = np.array([colx.get_array(), colx.get_array(), colx.get_array(), colx.get_array()], dtype=float)
    __vcolors = np.append(__vcolors, col, axis=0)

    __triangles = np.empty((0, 3)).astype(np.int32)
    __triangles = __append(__triangles, 0, 2, 1)
    __triangles = __append(__triangles, 0, 3, 2)
    __triangles = __append(__triangles, 5, 6, 4)
    __triangles = __append(__triangles, 6, 7, 4)
    __triangles = __append(__triangles, 2, 5, 1)
    __triangles = __append(__triangles, 5, 2, 6)
    __triangles = __append(__triangles, 1, 4, 0)
    __triangles = __append(__triangles, 1, 5, 4)
    __triangles = __append(__triangles, 4, 3, 0)
    __triangles = __append(__triangles, 4, 7, 3)
    __triangles = __append(__triangles, 6, 3, 7)
    __triangles = __append(__triangles, 6, 2, 3)
    return __vertices, __vcolors, __triangles


def matrix_to_vertices(matrix: np.ndarray, spalt: float = 1,
                       colx:EnumColor=EnumColor.r2w,
                       dxyz: Point = Point(0, 0, 0),
                       zoom: Point = Point(2, 1, 1),
                       sockel: float = -1
                       ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    converts a matrix into a point cloud, color description, and triangle

    Args:

        zoom:
        dxyz:
        spalt:
        colx:
        matrix:
        step_y:
        step_x:
        sockel:


    Returns:
        object:

    """

    __vertices = np.empty((0, 3)).astype(np.float64)
    __vcolors = np.empty((0, 3)).astype(np.float64)
    __date=None
    xi = 0.0
    yi = 0.0
    for x in matrix:
        for y in x:
            if isinstance(y, datetime):
                __date=y
            else:
                if isinstance(__date, datetime):
                    yy = (y * 10.0 - np.min(matrix[0:, 1:])) / (np.max(matrix[0:, 1:]) - np.min(matrix[0:, 1:]))
                else:
                    yy = (y * 10.0 - np.min(matrix)) / (np.max(matrix) - np.min(matrix))

                vert = np.array([[(xi + dxyz.x) * zoom.x, (yi + dxyz.y) * zoom.y, (sockel + dxyz.z) * zoom.z],
                                 [(xi + dxyz.x) * zoom.x, (yi + dxyz.y) * zoom.y, (yy + dxyz.z) * zoom.z],
                                 [(xi + dxyz.x + spalt) * zoom.x, (yi + dxyz.y) * zoom.y, (sockel + dxyz.z) * zoom.z],
                                 [(xi + dxyz.x + spalt) * zoom.x, (yi + dxyz.y) * zoom.y, (yy + dxyz.z) * zoom.z]],
                                dtype=float)
                __vertices = np.append(__vertices, vert, axis=0)

                col = Color(col=colx).get_color(yy/10).get_numpy_array()

                __vcolors = np.append(__vcolors, col, axis=0)
                __vcolors = np.append(__vcolors, col, axis=0)
                __vcolors = np.append(__vcolors, col, axis=0)
                __vcolors = np.append(__vcolors, col, axis=0)

                yi += 1
        yi = 0
        xi += 1
    if isinstance(__date, datetime):
        __triangles = __get_triangles(matrix[0:, 1:])
    else:
        __triangles = __get_triangles(matrix)
    return __vertices, __vcolors, __triangles


def matrix_to_vertices_quader(matrix: np.ndarray,
                              dxyz: Point = Point(0, 0, 20),
                              colx: EnumColor = EnumColor.b2w,
                              zoom: Point = Point(2, 1, 1),
                              sockel: float = -1
                              ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    converts a matrix into a point cloud, color description, and triangle

    

    """

    __vertices = None
    __vcolors = None
    __triangles = None
    __date=None

    xi = 0
    yi = 0
    for x in matrix:
        for y in x:
            if isinstance(y, datetime):
                __date = y
            else:
                if isinstance(__date, datetime):
                    yy = (y * 10.0 - np.min(matrix[0:, 1:])) / (np.max(matrix[0:, 1:]) - np.min(matrix[0:, 1:]))
                else:
                    yy = (y * 10.0 - np.min(matrix)) / (np.max(matrix) - np.min(matrix))

                vertices, vcolors, triangles = __get_quader(yy, dxyz=Point(yi +dxyz.x, xi+dxyz.y, 0+dxyz.z), colx=Color(col=colx).get_color(yy/10),sockel=sockel,zoom=zoom)
                __vertices, __vcolors, __triangles = __append_quader(__vertices, __vcolors, __triangles, vertices, vcolors,
                                                                     triangles)


            xi += 1
        xi = 0
        yi += 1
        vertices=vertices*zoom

    return __vertices, __vcolors, __triangles
