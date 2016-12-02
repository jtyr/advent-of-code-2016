#!/usr/bin/python

"""
--- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements,
and the clock's oscillator is regulated by stars. Unfortunately, the
stars have been stolen... by the Easter Bunny. To save Christmas, Santa
needs you to retrieve all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on
each day in the advent calendar; the second puzzle is unlocked when you
complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere.
"Near", unfortunately, is as close as you can get - the instructions on
the Easter Bunny Recruiting Document the Elves intercepted start here,
and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates
(where you just landed) and face North. Then, follow the provided
sequence: either turn left (L) or right (R) 90 degrees, then walk forward
the given number of blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though,
so you take a moment and work out the destination. Given that you can
only walk on the street grid of the city, how far is the shortest path to
the destination?

For example:

- Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks
  away.
- R2, R2, R2 leaves you 2 blocks due South of your starting position, which
  is 2 blocks away.
- R5, L5, R5, R3 leaves you 12 blocks away.

How many blocks away is Easter Bunny HQ?

--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting
Document. Easter Bunny HQ is actually at the first location you visit
twice.

For example, if your instructions are R8, R4, R4, R8, the first location
you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?
"""


def get_data():
    f = open("input/01.txt", "r")

    return f.read()


def walk(path, axis, steps, multi=1):
    last = path[-1]
    twice = None

    for n in range(1, steps + 1):
        if axis == 'x':
            record = {'x': last['x'] + (n * multi), 'y': last['y']}
        else:
            record = {'x': last['x'], 'y': last['y'] + (n * multi)}

        if record in path:
            twice = record

        path.append(record)

    return twice


def main():
    data = get_data()
    path = [{'x': 0, 'y': 0}]
    direction = 'N'
    twice_dist = None

    for seq in data.rstrip().split(', '):
        print(seq)
        site = seq[0]
        step = int(seq[1:])

        if direction == 'N' and site == 'L':
            t = walk(path, 'x', step, -1)
            direction = 'W'
        elif direction == 'N' and site == 'R':
            t = walk(path, 'x', step)
            direction = 'E'
        elif direction == 'S' and site == 'L':
            t = walk(path, 'x', step)
            direction = 'E'
        elif direction == 'S' and site == 'R':
            t = walk(path, 'x', step, -1)
            direction = 'W'
        elif direction == 'E' and site == 'L':
            t = walk(path, 'y', step)
            direction = 'N'
        elif direction == 'E' and site == 'R':
            t = walk(path, 'y', step, -1)
            direction = 'S'
        elif direction == 'W' and site == 'L':
            t = walk(path, 'y', step, -1)
            direction = 'S'
        elif direction == 'W' and site == 'R':
            t = walk(path, 'y', step)
            direction = 'N'

        if twice_dist is None and t is not None:
            twice_dist = abs(t['x']) + abs(t['y'])

    print("[Star 1] Disatance: %d" % (abs(path[-1]['x']) + abs(path[-1]['y'])))
    print("[Star 2] Disatance: %s" % (
        '???' if twice_dist is None else twice_dist))


if __name__ == '__main__':
    main()
