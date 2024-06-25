from dataclasses import dataclass
from typing import TypeAlias
from PIL import Image
from random import randint

from classroom import Classroom
from student import Student

EMPTY = 0
WALL = 1
EXIT = 2


@dataclass(slots=True)
class Tile:
    x: int
    y: int
    tiletype: int


Coordinate: TypeAlias = tuple[int, int]


class Map:
    _in: list[list[Tile]]
    _students: list[Student]
    _cycle: int

    __width: int
    __height: int
    __exits: list[Coordinate]
    __classrooms: dict[int, Classroom]

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__exits = []
        self.__classrooms = {}

        self._in = [[Tile(x, y, EMPTY) for x in range(width)] for y in range(height)]
        self._students = []
        self._cycle = 0

    def get(self, x: int, y: int) -> Tile:
        return self._in[y][x]

    def next_cycle(self) -> None:
        """increases the cycle by one and empties all classrooms"""
        self._cycle += 1
        for classroom in self.__classrooms.values():
            classroom.empty()

    @property
    def cycle(self) -> int:
        return self._cycle

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def size(self) -> Coordinate:
        return self.__width, self.__height

    @property
    def exits(self) -> list[Coordinate]:
        """returns a list of all exits in the map"""
        if self.__exits:
            return self.__exits

        for y in range(self.__height):
            for x in range(self.__width):
                if self.get(x, y).tiletype == EXIT:
                    self.__exits.append((x, y))
        return self.__exits

    def is_valid(self, point: Coordinate) -> bool:
        """determines if a given point is a valid space for a `Student` to be on"""

        # x check
        if not (self.__width > point[0] >= 0):
            return False

        # y check
        if not (self.__height > point[1] >= 0):
            return False

        # wall check
        if self.get(*point).tiletype not in {EXIT, EMPTY}:
            return False
        return True

    @property
    def students(self) -> list[Student]:
        return self._students

    def add_student(self, student: Student) -> None:
        self._students.append(student)

    def populate(self, amt: int) -> None:
        self._students = [Student.random(self.__classrooms) for _ in range(amt)]
        for student in self._students:
            student.x, student.y = student.classes[0].getnextpoint()

    @staticmethod
    def from_photo(img):
        # type: (Image.Image) -> Map
        """load a map from a PIL image"""
        img = img.convert("RGB")

        ret: Map = Map(img.width, img.height)
        for y in range(img.height):
            for x in range(img.width):
                match img.getpixel((x, y)):
                    case 0, 0, 0:
                        ret.get(x, y).tiletype = WALL
                    case 255, 255, 255:
                        ret.get(x, y).tiletype = EMPTY
                    case 0x7F, 0x7F, 0x7F:
                        ret.get(x, y).tiletype = EXIT
                    case r, g, b:
                        if r not in ret.__classrooms:
                            ret.__classrooms[r] = Classroom(len(ret.__classrooms) + 1)
                        if g == 0:
                            if b == 0:
                                ret.__classrooms[r].nw = x, y
                            else:
                                ret.__classrooms[r].se = x, y
                            ret.get(x, y).tiletype = WALL
                        else:
                            ret.get(x, y).tiletype = EMPTY

        return ret
