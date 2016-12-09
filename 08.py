#!/usr/bin/python

"""
--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an
implementation of two-factor authentication after a long game of
requirements telephone.

To get past the door, you first swipe a keycard (no problem; there was
one on a nearby desk). Then, it displays a code on a little screen, and
you type that code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've
taken everything apart and figured out how it works. Now you just have to
work out what the screen would have displayed.

The magnetic strip on the card you swiped encodes a series of
instructions for the screen; these instructions are your puzzle input.
The screen is 50 pixels wide and 6 pixels tall, all of which start off,
and is capable of three somewhat peculiar operations:

- rect AxB turns on all of the pixels in a rectangle at the top-left of
  the screen which is A wide and B tall.

- rotate row y=A by B shifts all of the pixels in row A (0 is the top
  row) right by B pixels. Pixels that would fall off the right end appear
  at the left end of the row.

- rotate column x=A by B shifts all of the pixels in column A (0 is the
  left column) down by B pixels. Pixels that would fall off the bottom
  appear at the top of the column.

For example, here is a simple sequence on a smaller screen:

- rect 3x2 creates a small rectangle in the top-left corner:

###....
###....
.......

- rotate column x=1 by 1 rotates the second column down by one pixel:

#.#....
###....
.#.....

- rotate row y=0 by 4 rotates the top row right by four pixels:

....#.#
###....
.#.....

- rotate column x=1 by 1 again rotates the second column down by one
  pixel, causing the bottom pixel to wrap back to the top:

.#..#.#
#.#....
.#.....

As you can see, this display technology is extremely powerful, and will
soon dominate the tiny-code-displaying-screen market. That's what the
advertisement on the back of the display tries to convince you, anyway.

There seems to be an intermediate check of the voltage used by the
display: after you swipe your card, if the screen did work, how many
pixels should be lit?

--- Part Two ---

You notice that the screen is only capable of displaying capital letters;
in the font it uses, each letter is 5 pixels wide and 6 tall.

After you swipe your card, what code is the screen trying to display?
"""


import re
import sys


def get_data(name):
    f = open(name, 'r')

    return f.readlines()


def print_screen(screen, prnt=True):
    cnt = 0

    for row in screen:
        for col in row:
            if col:
                if prnt:
                    sys.stdout.write('#')
                cnt += 1
            else:
                if prnt:
                    sys.stdout.write('.')

        if prnt:
            print('')

    if prnt:
        print('---')

    return cnt


def rect(screen, x, y):
    for i in range(y):
        for j in range(x):
            screen[i][j] = True


def rotate_row(screen, row, by):
    for _ in range(by):
        last = len(screen[row]) - 1
        tmp = screen[row][last]

        for i in reversed(range(len(screen[row]))):
            if i > 0:
                screen[row][i] = screen[row][i-1]
            else:
                screen[row][i] = tmp


def rotate_col(screen, col, by):
    for _ in range(by):
        last = len(screen) - 1
        tmp = screen[last][col]

        for i in reversed(range(len(screen))):
            if i > 0:
                screen[i][col] = screen[i-1][col]
            else:
                screen[i][col] = tmp


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <input_file>" % sys.argv[0])
        sys.exit(1)

    data = get_data(sys.argv[1])
    cnt1 = 0
    p_rect = re.compile('^rect (\d+)x(\d+)$')
    p_rotate_row = re.compile('^rotate row y=(\d+) by (\d+)$')
    p_rotate_col = re.compile('^rotate column x=(\d+) by (\d+)$')
    screen = [[False] * 50 for _ in range(6)]

    for line in data:
        m_rect = p_rect.match(line)
        m_rotate_row = p_rotate_row.match(line)
        m_rotate_col = p_rotate_col.match(line)

        if m_rect is not None:
            rect(screen, *map(int, m_rect.groups()))
        elif m_rotate_row is not None:
            rotate_row(
                screen, *map(int, m_rotate_row.groups()))
        elif m_rotate_col is not None:
            rotate_col(
                screen, *map(int, m_rotate_col.groups()))

    cnt1 = print_screen(screen, False)

    print("[Star 1] Number of LEDs on: %s" % cnt1)
    print("[Star 2] Message:")
    print_screen(screen)


if __name__ == '__main__':
    main()
