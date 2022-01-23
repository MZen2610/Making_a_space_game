from itertools import cycle
from curses_tools import draw_frame, read_controls, get_frame_size

import asyncio
import curses
import random
import time


def calculate_displacement(canvas, row, column, frame, height, width):
    row_frame, column_frame = get_frame_size(frame)
    rows_direction, columns_direction, space_pressed = read_controls(canvas)

    if 0 < row + rows_direction < height - row_frame:
        row = row + rows_direction

    if 0 < column + columns_direction < width - column_frame:
        column = column + columns_direction

    return canvas, row, column


async def animate_spaceship(canvas, height, width, frame1, frame2):
    column = int(width / 2)
    row = int(height / 4)

    for item in cycle([frame1, frame2]):
        frame = frame1 if item == frame1 else frame2
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)
        canvas, row, column = calculate_displacement(canvas, row, column, frame, height, width)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for step in range(2):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for step in range(2):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def draw(canvas):
    curses.curs_set(False)
    canvas.border()

    coroutines_stars = []
    coroutines_fire = []
    coroutines_star_ship = []

    symbols = '+*.:'
    count_stars = random.randint(50, 75)
    height, width = canvas.getmaxyx()
    half_width = int(width / 2)
    retreat = 2

    with open('animations/rocket_frame_1.txt', 'r') as rocket_frame_1:
        frame1 = rocket_frame_1.read()
    with open('animations/rocket_frame_2.txt', 'r') as rocket_frame_2:
        frame2 = rocket_frame_2.read()

    for star in range(count_stars):
        row = random.randint(1, height - retreat)
        column = random.randint(1, width - retreat)
        symbol = random.choice(symbols)
        flashing_star = blink(canvas, row, column, symbol)
        coroutines_stars.append(flashing_star)

    coroutines_fire.append(fire(canvas, 1, half_width, 1))
    coroutines_star_ship.append(animate_spaceship(canvas, height, width, frame1, frame2))

    coroutines = coroutines_stars + coroutines_fire + coroutines_star_ship

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break

        canvas.nodelay(True)
        canvas.refresh()
        time.sleep(0.3)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
