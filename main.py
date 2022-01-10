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

    while True:
        step = [1, 2]
        for item in cycle(step):
            frame = frame2
            negative_frame = frame1
            if item == 1:
                frame = frame1
                negative_frame = frame2

            draw_frame(canvas, row, column, negative_frame, negative=True)
            canvas, row, column = calculate_displacement(canvas, row, column, frame, height, width)
            draw_frame(canvas, row, column, frame)
            canvas.refresh()

            await asyncio.sleep(0)


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
        sequence = random.randint(1, 2)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)

        if sequence == 1:
            canvas.addstr(row, column, symbol)
            await asyncio.sleep(0)
            await asyncio.sleep(0)
            await asyncio.sleep(0)
        elif sequence == 2:
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            await asyncio.sleep(0)
        else:
            canvas.addstr(row, column, symbol)
            await asyncio.sleep(0)


def draw(canvas):
    curses.curs_set(False)
    canvas.border()

    coroutines = []
    coroutines_fire = []
    coroutines_star_ship = []

    symbols = '+*.:'
    count_stars = random.randint(50, 75)
    height, width = canvas.getmaxyx()
    half_width = int(width / 2)

    with open('animations/rocket_frame_1.txt', 'r') as rocket_frame_1:
        frame1 = rocket_frame_1.read()
    with open('animations/rocket_frame_2.txt', 'r') as rocket_frame_2:
        frame2 = rocket_frame_2.read()

    while count_stars > 0:
        row = random.randint(1, height - 2)
        column = random.randint(1, width - 2)
        symbol = random.choice(symbols)
        star = blink(canvas, row, column, symbol)
        coroutines.append(star)
        count_stars -= 1

    coroutines_fire.append(fire(canvas, 1, half_width, 1))
    coroutines_star_ship.append(animate_spaceship(canvas, height, width, frame1, frame2))

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

        for coroutine in coroutines_fire.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines_fire.remove(coroutine)
        if len(coroutines_fire) == 0:
            break

        for coroutine in coroutines_star_ship.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines_star_ship.remove(coroutine)
        if len(coroutines_star_ship) == 0:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
