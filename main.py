from itertools import cycle
from curses_tools import draw_frame, read_controls

import asyncio
import curses
import random
import time


async def animate_spaceship(canvas, row, column, frame1, frame2):
    while True:
        frame = [1, 2]
        for item in cycle(frame):
            if item == 1:
                rows_direction, columns_direction, space_pressed = read_controls(canvas)
                draw_frame(canvas, row, column, frame2, negative=True)
                row = row + rows_direction
                column = column + columns_direction
                draw_frame(canvas, row, column, frame1)
                canvas.refresh()

                await asyncio.sleep(0)
            elif item == 2:
                rows_direction, columns_direction, space_pressed = read_controls(canvas)
                draw_frame(canvas, row, column, frame1, negative=True)
                row = row + rows_direction
                column = column + columns_direction
                draw_frame(canvas, row, column, frame2)
                canvas.refresh()

                await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

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
    coroutines = []
    coroutines_fire = []
    coroutines_star_ship = []
    symbols = '+*.:'
    count_stars = random.randint(50, 75)
    height, width = canvas.getmaxyx()
    with open('animations/rocket_frame_1.txt', 'r') as rocket_frame_1:
        frame1 = rocket_frame_1.read()
    with open('animations/rocket_frame_2.txt', 'r') as rocket_frame_2:
        frame2 = rocket_frame_2.read()
    half_width = int(width / 2)
    quarter_height = int(height / 4)

    curses.curs_set(False)
    canvas.border()

    while count_stars > 0:
        row = random.randint(1, height - 2)
        column = random.randint(1, width - 2)
        symbol = random.choice(symbols)
        star = blink(canvas, row, column, symbol)
        coroutines.append(star)
        count_stars -= 1

    for step in range(height):
        coroutines_fire.append(fire(canvas, 1, half_width, 1))

    for step in range(1, 2):
        coroutines_star_ship.append(animate_spaceship(canvas, quarter_height,   half_width, frame1, frame2))

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

        # for coroutine in coroutines_fire.copy():
        #     try:
        #         coroutine.send(None)
        #     except StopIteration:
        #         coroutines_fire.remove(coroutine)
        # if len(coroutines_fire) == 0:
        #     break

        for coroutine in coroutines_star_ship.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines_star_ship.remove(coroutine)
        if len(coroutines_star_ship) == 0:
            break
        # canvas.refresh()
        # time.sleep(0.3)
        #read_controls(canvas)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
