#!/usr/bin/python

"""
--- Day 12: Leonardo's Monorail ---

You finally reach the top floor of this building: a garden with a slanted
glass ceiling. Looks like there are no more stars to be had.

While sitting on a nearby bench amidst some tiger lilies, you manage to
decrypt some of the files you extracted from the servers downstairs.

According to these documents, Easter Bunny HQ isn't just this building -
it's a collection of buildings in the nearby area. They're all connected
by a local monorail, and there's another building not far from here!
Unfortunately, being night, the monorail is currently not operating.

You remotely connect to the monorail control systems and discover that
the boot sequence expects a password. The password-checking logic (your
puzzle input) is easy to extract, but the code it uses is strange: it's
assembunny code designed for the new computer you just assembled. You'll
have to execute the code and get the password.

The assembunny code you've extracted operates on four registers (a, b, c,
and d) that start at 0 and can hold any integer. However, it seems to
make use of only a few instructions:

- cpy x y copies x (either an integer or the value of a register) into
  register y.
- inc x increases the value of register x by one.
- dec x decreases the value of register x by one.
- jnz x y jumps to an instruction y away (positive means forward; negative
  means backward), but only if x is not zero.

The jnz instruction moves relative to itself: an offset of -1 would
continue at the previous instruction, while an offset of 2 would skip
over the next instruction.

For example:

cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a

The above code would set register a to 41, increase its value by 2,
decrease its value by 1, and then skip the last dec a (because a is not
zero, so the jnz a 2 skips it), leaving register a at 42. When you move
past the last instruction, the program halts.

After executing the assembunny code in your puzzle input, what value is
left in register a?

--- Part Two ---

As you head down the fire escape to the monorail, you notice it didn't
start; register c needs to be initialized to the position of the ignition
key.

If you instead initialize register c to be 1, what value is now left in
register a?
"""


import sys
from time import sleep


def get_data(name):
    f = open(name, 'r')

    return f.readlines()


def run_cmd(pos, data, regs):
    fields = data[pos].rstrip().split()

    if fields[0] == 'cpy':
        if fields[1] in regs.keys():
            regs[fields[2]] = regs[fields[1]]
        else:
            regs[fields[2]] = int(fields[1])
    elif fields[0] == 'inc':
        regs[fields[1]] += 1
    elif fields[0] == 'dec':
        regs[fields[1]] -= 1
    elif fields[0] == 'jnz':
        if (
                (
                    fields[1] in regs.keys() and
                    regs[fields[1]] != 0
                ) or (
                    fields[1] not in regs.keys() and
                    int(fields[1]) != 0
                )):
            pos += int(fields[2])-1

    pos += 1

    return pos


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <input_file>" % sys.argv[0])
        sys.exit(1)

    data = get_data(sys.argv[1])
    regs = {
        'a': 0,
        'b': 0,
        'c': 0,
        'd': 0
    }
    pos = 0

    while pos < len(data):
        pos = run_cmd(pos, data, regs)

    print("[Star 1] Value in register a: %d" % regs['a'])

    regs = {
        'a': 0,
        'b': 0,
        'c': 1,
        'd': 0
    }
    pos = 0

    while pos < len(data):
        pos = run_cmd(pos, data, regs)

    print("[Star 2] Value in register a: %d" % regs['a'])


if __name__ == '__main__':
    main()
