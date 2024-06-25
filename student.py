from dataclasses import dataclass, field
from random import choices, choice
from typing import Any, Callable, Self, TypeAlias

from classroom import Classroom

Coordinate: TypeAlias = tuple[int, int]

YELLOW = "#F59E0B"

with open("resources/firstnames.txt") as f:
    FIRSTS = f.read().splitlines()
with open("resources/lastnames.txt") as f:
    LASTS = f.read().splitlines()


@dataclass
class Student:
    x: int
    y: int
    name: str
    path: list[Coordinate] = field(init=False, default_factory=list)
    classes: list[Classroom] = field(init=False, default_factory=list)

    def draw(
        self,
        canvas,
        height: int,
        width: int,
        on_click: Callable[[Self], Any],
    ) -> None:
        """draws itself on `canvas` at its current location and `tag_bind`s the square to `on_click`"""
        id = canvas.create_rectangle(
            self.x * width,
            self.y * height,
            self.x * width + width,
            self.y * height + height,
            fill=YELLOW,
            width=0,
        )
        canvas.tag_bind(id, "<Button-1>", lambda *args: on_click(self))

    def move(self) -> None:
        """continue on the path towards the destination"""
        if not self.path:
            return
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.path.pop(0)

    @property
    def location(self) -> Coordinate:
        return self.x, self.y

    @staticmethod
    def random(possible_classes):
        # type: (dict[int, Classroom]) -> Student
        """generate a `Student` at (0, 0) with a random schedule"""
        ret = Student(0, 0, f"{choice(FIRSTS)} {choice(LASTS)}")
        ret.classes = choices(list(possible_classes.values()), k=7)

        return ret
