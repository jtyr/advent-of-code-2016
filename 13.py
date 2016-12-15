#!/usr/bin/python

"""
--- Day 13: A Maze of Twisty Little Cubicles ---

You arrive at the first floor of this new building to discover a much
less welcoming environment than the shiny atrium of the last one.
Instead, you are in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative
integers (x,y). Each such coordinate is either a wall or an open space.
You can't move diagonally. The cube maze starts at 0,0 and seems to
extend infinitely toward positive x and y; negative values are invalid,
as they represent a location outside the building. You are in a small
waiting area at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains, the
layout is actually quite logical. You can determine whether a given x,y
coordinate will be a wall or an open space using a simple system:

- Find x*x + 3*x + 2*x*y + y + y*y.
- Add the office designer's favorite number (your puzzle input).
- Find the binary representation of that sum; count the number of bits that
  are 1.
  - If the number of bits that are 1 is even, it's an open space.
  - If the number of bits that are 1 is odd, it's a wall.

For example, if the office designer's favorite number were 10, drawing
walls as # and open spaces as ., the corner of the building containing
0,0 would look like this:

  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###

Now, suppose you wanted to reach 7,4. The shortest route you could take
is marked as O:

  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###

Thus, reaching 7,4 would take a minimum of 11 steps (starting from your
current location, 1,1).

What is the fewest number of steps required for you to reach 31,39?

--- Part Two ---

How many locations (distinct x,y coordinates, including your starting
location) can you reach in at most 50 steps?
"""


import sys
from time import sleep


def get_data(name):
    f = open(name, 'r')

    return f.read()


def print_map(fav_num, pos_x, pos_y, pos_list):
    for y in range(fav_num):
        for x in range(fav_num):
            bin_num = len("{0:b}".format(
                x*x + 3*x + 2*x*y + y + y*y + fav_num).replace('0', ''))

            if (x, y) in pos_list:
                sys.stdout.write("O")
            elif x == 1 and y == 1:
                sys.stdout.write("A")
            elif x == pos_x and y == pos_y:
                sys.stdout.write("B")
            elif bin_num % 2 == 0:
                sys.stdout.write(".")
            else:
                sys.stdout.write("#")

        print("")


def is_not_wall(fav_num, x, y):
    bin_num = len("{0:b}".format(
        x*x + 3*x + 2*x*y + y + y*y + fav_num).replace('0', ''))

    if bin_num % 2 == 0:
        return True
    else:
        return False


def walk(
        test, level, fav_num, pos_x, pos_y, pos_list, max_steps, pos_visited,
        x, y):
    if test:
        sleep(0.1)
        print("%s(%d, %d)" % (' '*level, x, y))

    if len(pos_list) <= max_steps and "%d;%d" % (x, y) not in pos_visited:
        pos_visited["%d;%d" % (x, y)] = 1

    if x == pos_x and y == pos_y:
        pos_list.append((x, y))

        if test:
            print("%sReached final position" % (' '*level))

        return True, pos_list

    if (x, y) in pos_list:
        if test:
            print("%sRepetitive position" % (' '*level))

        return False, pos_list

    pos_lists = []

    if x-1 >= 0 and is_not_wall(fav_num, x-1, y):
        pos_list1 = list(pos_list)
        pos_list1.append((x, y))
        reached, new_pos_list1 = walk(
            test, level+1, fav_num, pos_x, pos_y, pos_list1, max_steps,
            pos_visited, x-1, y)

        if reached:
            pos_lists.append(new_pos_list1)

    if x+1 < fav_num and is_not_wall(fav_num, x+1, y):
        pos_list2 = list(pos_list)
        pos_list2.append((x, y))
        reached, new_pos_list2 = walk(
            test, level+1, fav_num, pos_x, pos_y, pos_list2, max_steps,
            pos_visited, x+1, y)

        if reached:
            pos_lists.append(new_pos_list2)

    if y-1 >= 0 and is_not_wall(fav_num, x, y-1):
        pos_list3 = list(pos_list)
        pos_list3.append((x, y))
        reached, new_pos_list3 = walk(
            test, level+1, fav_num, pos_x, pos_y, pos_list3, max_steps,
            pos_visited, x, y-1)

        if reached:
            pos_lists.append(new_pos_list3)

    if y+1 < fav_num and is_not_wall(fav_num, x, y+1):
        pos_list4 = list(pos_list)
        pos_list4.append((x, y))
        reached, new_pos_list4 = walk(
            test, level+1, fav_num, pos_x, pos_y, pos_list4, max_steps,
            pos_visited, x, y+1)

        if reached:
            pos_lists.append(new_pos_list4)

    pos_lists_lengths = list(map(len, pos_lists))
    shortest = None

    if len(pos_lists_lengths):
        max_len = max(pos_lists_lengths)
        shortest = pos_lists_lengths.index(max_len)

    for i, length in enumerate(pos_lists_lengths):
        if length > len(pos_list) and length < max_len:
            max_len = length
            shortest = i

    if shortest is None:
        return False, pos_list
    else:
        return True, pos_lists[shortest]


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <input_file>" % sys.argv[0])
        sys.exit(1)

    fav_num = int(get_data(sys.argv[1]))
    pos_list_start = []
    test = False
    max_steps = 50
    pos_visited = {}

    if '_test' in sys.argv[1]:
        test = True

    if test:
        pos_x, pos_y = 7, 4
    else:
        pos_x, pos_y = 31, 39

    if test:
        print_map(fav_num, pos_x, pos_y, pos_list_start)

    reached, pos_list = walk(
        test, 0, fav_num, pos_x, pos_y, pos_list_start, max_steps, pos_visited,
        1, 1)

    if test:
        print_map(fav_num, pos_x, pos_y, pos_list)

    print("[Star 1] Number of steps: %d" % (len(pos_list) - 1))
    print(
        "[Star 2] Number of positions visited in max 50 steps: %d" %
        len(pos_visited))


if __name__ == '__main__':
    main()
