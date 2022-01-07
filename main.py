import time
import curses
import asyncio
import random


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
    symbols = '+*.:'
    count_stars = random.randint(50, 75)
    height, width = canvas.getmaxyx()

    while count_stars > 0:
        row = random.randint(1, height - 2)
        column = random.randint(1, width - 2)
        symbol = random.choice(symbols)
        star = blink(canvas, row, column, symbol)
        coroutines.append(star)
        count_stars -= 1

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)

            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break
        canvas.refresh()
        time.sleep(0.3)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
