from __future__ import annotations

import warnings
from enum import Enum

import numpy as np


class Point:
    _x: float
    _y: float
    _z: float

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        """
         Args:
            x:
                value X
            y:
                value y
            z:
                value z
        """
        self._x = x
        self._y = y
        self._z = z

    def get_array(self) -> np.ndarray:
        """
        Returns:
            np.ndarray:
                as [x,y,z] 
        """
        return np.array([self._x, self._y, self._z], dtype=float)

    @property
    def x(self) -> float:
        """
        Returns:
            float:
                x value
        """
        return self._x

    @property
    def y(self) -> float:
        """
        Returns:
            float:
                y value
        """
        return self._y

    @property
    def z(self) -> float:
        """
        Returns:
            float:
                z value
        """
        return self._z


class EnumColor(Enum):
    r2w = 1
    g2w = 2
    b2w = 3
    gr2w = 4
    r2b=5


class Color:
    def __init__(self, r: float = 0, g: float = 0, b: float = 0, col: EnumColor = EnumColor.b2w) -> None:
        """
        Create a Color r,g,b Class
        Args:
            r:
                value 0-1
            g:
                value 0-1
            b:
                value 0-1
        """
        self._r = r
        self._g = g
        self._b = b
        self._col = col

    def get_color(self, x: float = 1) -> Color:
        if self._col.value == EnumColor.r2w.value:
            return self._get_red(x)
        elif self._col.value == EnumColor.g2w.value:
            return self._get_green(x)
        elif self._col.value == EnumColor.b2w.value:
            return self._get_blue(x)
        elif self._col.value == EnumColor.r2b.value:
            if x>0.5:
                return self._get_red((x-0.5)*2)
            else:
                return self._get_blue(1-(x*2))
        else:
            return self._get_gray(x)

    def _get_blue(self, x: float = 1) -> Color:
        """
        Return a Color Class
        Args:
            x:
                0-1 value from white=0 to Blue =1
        Returns:
            Color Class
        """
        return Color(self._f2(x), self._f3(x), self._f1())

    def _get_green(self, x: float = 1):
        """
        Return a Color Class
        Args:
            x:
                0-1 value from White=0 to green =1
        Returns:
            Color Class
        """
        return Color(self._f3(x), self._f1(), self._f2(x))

    def _get_red(self, x: float = 1):
        """
        Return a Color Class
        Args:
            x:
                0-1 value from white=0 to red =1
        Returns:
            Color Class
        """
        return Color(self._f1(), self._f2(x), self._f3(x))

    def _get_gray(self, x: float = 1):
        """
        Return a Color Class
        Args:
            x:
                0-1 value from white=0 to black =1
        Returns:
            Color Class
        """
        x = self._check_null_bis_eins(x)
        return Color(1 - x, 1 - x, 1 - x)

    @staticmethod
    def _check_null_bis_eins(x: float) -> float:
        """
            Check and adjust value x to 0-1
        Args:
            x:
        Returns:
            value 0-1
        """
        if x < 0:
            warnings.warn('Value should by 0-1 not ' + str(x))
            x = 0
        if x > 1:
            x = 1
            warnings.warn('Value should by 0-1 not ' + str(x))
        return x

    def _f1(self) -> float:
        """
        Helper Function
        Returns:
            returns the value from 0-1 for make color
        """
        _y = 1
        _y = self._check_null_bis_eins(_y)
        return _y

    def _f2(self, x):
        """
        Helper Function
        Returns:
            returns the value from 0-1 for make color
        """
        _y = -x + 1
        _y = self._check_null_bis_eins(_y)
        return _y

    def _f3(self, x):
        """
        Helper Function
        Returns:
            returns the value from 0-1 for make color
        """
        _y = -x + 1
        _y = self._check_null_bis_eins(_y)
        return _y

    def __str__(self) -> str:
        """
        Returns:
            str:
                class Color as String r,g,b in 0-1
        """
        return str(self._r) + ' ' + str(self._g) + ' ' + str(self._b)

    def get_numpy_array(self) -> np.ndarray:
        """
        Returns:
            np.ndarray:
                as [[r,g,b]] in 0-1
        """
        return np.array([[self._r, self._g, self._b]], dtype=float)

    def get_array(self):
        """
        Returns:
            np.ndarray:
                as [r,g,b] in 0-1
        """
        return np.array([self._r, self._g, self._b], dtype=float)

