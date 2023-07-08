import sys
import time

import numpy as np
from scipy.spatial.transform import Rotation


class Cube:
    def __init__(self, width: int, bg: str = ' ', distance: int = 100, speed: float = 0.6):
        self.__angles: np.array = np.array([0, 0, 0], dtype=float)

        self.__width: int = width
        self.__screen_width: int = 160
        self.__screen_height: int = 44

        self.__bg: str = bg
        self.__z_buffer: list[float] = [0] * self.__screen_width * self.__screen_height
        self.__buffer: list[str] = [self.__bg] * self.__screen_width * self.__screen_height

        self.__distance: int = distance
        self.__h_offset: float = -2 * self.__width
        self.__k1: float = 40

        self.__speed: float = speed

    def __rotate_point(self, x: float, y: float, z: float) -> np.array:
        rot = Rotation.from_euler('zyx', self.__angles, degrees=True)
        return rot.apply([x, y, z])

    def __rotate_face(self, c_x: float, c_y: float, c_z: float, ch: str) -> None:
        x, y, z = self.__rotate_point(c_x, c_y, c_z)
        z += self.__distance

        xp = int(self.__screen_width / 2 + self.__h_offset + 2 * self.__k1 * x / z)
        yp = int(self.__screen_height / 2 + self.__k1 * y / z)

        ooz = 1 / z
        i = xp + yp * self.__screen_width
        if 0 <= i < len(self.__z_buffer) and ooz > self.__z_buffer[i]:
            self.__z_buffer[i] = ooz
            self.__buffer[i] = ch

    def update(self) -> None:
        self.__z_buffer: list[float] = [0] * self.__screen_width * self.__screen_height
        self.__buffer: list[str] = [self.__bg] * self.__screen_width * self.__screen_height

        x = -self.__width
        while x < self.__width:
            y = -self.__width
            while y < self.__width:
                self.__rotate_face(x, y, -self.__width, '@')
                self.__rotate_face(self.__width, y, x, '$')
                self.__rotate_face(-self.__width, y, -x, '~')
                self.__rotate_face(-x, y, self.__width, '#')
                self.__rotate_face(x, -self.__width, -y, ';')
                self.__rotate_face(x, self.__width, -y, '+')

                y += self.__speed

            x += self.__speed

        self.__angles += np.array([0.5, 0.5, 0.15])

    def draw(self) -> None:
        for n, c in enumerate(self.__buffer):
            sys.stdout.write(c if n % self.__screen_width else '\n')


if __name__ == '__main__':
    cube = Cube(20, speed=1)

    try:
        sys.stdout.write('\x1b[2J')
        while True:
            sys.stdout.write('\x1b[H')

            cube.update()
            cube.draw()
            
            time.sleep(0.02)
    except KeyboardInterrupt:
        sys.exit()
