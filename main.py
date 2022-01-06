import time
import curses
import asyncio


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def draw(canvas):
    curses.curs_set(False)
    canvas.border()

    star_5_5 = blink(canvas, 5, 5, symbol='*')
    star_5_10 = blink(canvas, 5, 10, symbol='*')
    star_5_15 = blink(canvas, 5, 15, symbol='*')
    star_5_20 = blink(canvas, 5, 20, symbol='*')
    star_5_25 = blink(canvas, 5, 25, symbol='*')

    coroutines = [star_5_5, star_5_10, star_5_15, star_5_20, star_5_25]

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break
        canvas.refresh()
        time.sleep(1)

    # row, column = (5, 20)
    #
    # coroutine = blink(canvas, row, column, symbol='*')
    # while True:
    #     try:
    #         coroutine.send(None)
    #         canvas.refresh()
    #         time.sleep(1)
    #     except StopIteration:
    #         break

    # canvas.addstr(row, column, '*', curses.A_DIM)
    # canvas.refresh()
    # time.sleep(2)
    #
    # canvas.addstr(row, column, '*')
    # canvas.refresh()
    # time.sleep(0.3)
    #
    # canvas.addstr(row, column, '*', curses.A_BOLD)
    # canvas.refresh()
    # time.sleep(0.5)
    #
    # canvas.addstr(row, column, '*')
    # canvas.refresh()
    # time.sleep(0.3)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
