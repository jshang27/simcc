from dataclasses import dataclass
from random import randint
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]


@dataclass
class Classroom:
    id: int

    nw: Coordinate = 0, 0
    se: Coordinate = 0, 0

    num_students: int = 0

    def empty(self) -> None:
        """empties the classroom"""
        self.num_students = 0

    def getnextpoint(self) -> Coordinate:
        """get the next point a `Student` should occupy in a classroom"""
        row, col = divmod(self.num_students, (self.se[0] - self.nw[0]) >> 1)
        self.num_students += 1

        x = self.nw[0] + 2 + 2 * col
        y = self.nw[1] + 2 + 2 * row
        return x, y
