import tkinter as tk
from typing import Callable
from PIL import Image
from time import perf_counter_ns

from map import Map
from student import Student
from astar import a_star, squaredistance

selected: Student | None = None
"""the current selected student"""


def draw_map(
    map: Map, canvas: tk.Canvas, square_width: int, square_height: int
) -> None:
    """draw a `map` on `canvas`"""
    for y in range(map.height):
        for x in range(map.width):
            color = ["white", "black", "grey"][map.get(x, y).tiletype]

            canvas.create_rectangle(
                x * square_width,
                y * square_height,
                x * square_width + square_width,
                y * square_height + square_height,
                width=0,
                fill=color,
            )


def select(
    student: Student, current_name: tk.StringVar, current_schedule: tk.StringVar
) -> None:
    """set `selected` to a `Student`"""
    global selected
    selected = student

    current_name.set(selected.name)

    cblock = ""
    for classroom in selected.classes:
        cblock += f"Room {classroom.id}\n"

    current_schedule.set(cblock)


def draw_students(
    map: Map,
    canvas: tk.Canvas,
    square_width: int,
    square_height: int,
    on_click: Callable[[Student], None],
) -> None:
    """draw every `Student` in `map` on `canvas`"""
    for student in map.students:
        student.draw(canvas, square_height, square_width, on_click)


def update(
    root: tk.Tk,
    map: Map,
    canvas: tk.Canvas,
    square_width: int,
    square_height: int,
    current_name: tk.StringVar,
    current_schedule: tk.StringVar,
) -> None:
    """called every frame"""
    canvas.delete("all")
    draw_map(map, canvas, square_width, square_height)
    draw_students(
        map,
        canvas,
        square_width,
        square_height,
        lambda x: select(x, current_name, current_schedule),
    )

    # highlight the selected student's destination and current location
    if selected is not None:
        if len(selected.path) > 0:
            goal = selected.path[-1]
            canvas.create_rectangle(
                goal[0] * square_width,
                goal[1] * square_height,
                goal[0] * square_width + square_width,
                goal[1] * square_height + square_height,
                fill="#16A34A",  # green
                width=0,
            )
        canvas.create_rectangle(
            selected.x * square_width,
            selected.y * square_height,
            selected.x * square_width + square_width,
            selected.y * square_height + square_height,
            fill="#B91C1C",  # red
            width=0,
        )

    for student in map.students:
        student.move()
    root.after(
        100,
        update,
        root,
        map,
        canvas,
        square_width,
        square_height,
        current_name,
        current_schedule,
    )


def change_classes(root: tk.Tk, map: Map, current_block: tk.IntVar):
    """called every 30 seconds to switch to the next block"""
    map.next_cycle()
    current_block.set(current_block.get() + 1)

    if map.cycle >= 7:
        start = perf_counter_ns()
        for student in map.students:
            closest = min(map.exits, key=lambda x: squaredistance(x, student.location))
            student.path = a_star(
                student.location, closest, lambda x: squaredistance(closest, x), map
            )
        print(f"took {(perf_counter_ns() - start) / 1e6} ms to calc")
        return

    start = perf_counter_ns()
    for student in map.students:
        goal = student.classes[map.cycle].getnextpoint()
        student.path = a_star(
            student.location, goal, lambda x: squaredistance(goal, x), map
        )
    print(f"took {(perf_counter_ns() - start) / 1e6} ms to calc")

    root.after(30 * 1000, change_classes, root, map, current_block)


def main() -> int:
    root = tk.Tk()
    root.title("CC")
    root.geometry("900x350")

    root.columnconfigure(2, weight=1)

    map = Map.from_photo(Image.open("resources/map.png"))

    canvas = tk.Canvas(root, width=700, height=300)
    canvas.grid(row=0, column=0, columnspan=2, rowspan=2)

    current_block = tk.IntVar(root, 0)
    tk.Label(root, text="Block: ").grid(row=2, column=0)
    tk.Label(root, textvariable=current_block).grid(row=2, column=1)

    current_name = tk.StringVar(root, "None selected")
    tk.Label(root, textvariable=current_name).grid(row=0, column=2)
    current_schedule = tk.StringVar(root, "")
    tk.Label(root, textvariable=current_schedule).grid(row=1, column=2)

    square_height = 300 // map.height
    square_width = 700 // map.width

    map.populate(250)

    root.after(
        100,
        update,
        root,
        map,
        canvas,
        square_width,
        square_height,
        current_name,
        current_schedule,
    )
    root.after(2 * 1000, change_classes, root, map, current_block)
    root.mainloop()

    return 0


exit(main())
