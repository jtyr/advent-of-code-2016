#!/usr/bin/python

"""
--- Day 17: Two Steps Forward ---

You're trying to access a secure vault protected by a 4x4 grid of small
rooms connected by doors. You start in the top-left room (marked S), and
you can access the vault (marked V) once you reach the bottom-right room:

#########
#S| | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | |V#
#########

Fixed walls are marked with #, and doors are marked with - or |.

The doors in your current room are either open or closed (and locked)
based on the hexadecimal MD5 hash of a passcode (your puzzle input)
followed by a sequence of uppercase characters representing the path you
have taken so far (U for up, D for down, L for left, and R for right).

Only the first four characters of the hash are used; they represent,
respectively, the doors up, down, left, and right from your current
position. Any b, c, d, e, or f means that the corresponding door is open;
any other character (any number or a) means that the corresponding door
is closed and locked.

To access the vault, all you need to do is reach the bottom-right room;
reaching this room opens the vault and all doors in the maze.

For example, suppose the passcode is hijkl. Initially, you have taken no
steps, and so your path is empty: you simply find the MD5 hash of hijkl
alone. The first four characters of this hash are ced9, which indicate
that up is open (c), down is open (e), left is open (d), and right is
closed and locked (9). Because you start in the top-left corner, there
are no "up" or "left" doors to be open, so your only choice is down.

Next, having gone only one step (down, or D), you find the hash of
hijklD. This produces f2bc, which indicates that you can go back up, left
(but that's a wall), or right. Going right means hashing hijklDR to get
5745 - all doors closed and locked. However, going up instead is
worthwhile: even though it returns you to the room you started in, your
path would then be DU, opening a different set of doors.

After going DU (and then hashing hijklDU to get 528e), only the right
door is open; after going DUR, all doors lock. (Fortunately, your actual
passcode is not hijkl).

Passcodes actually used by Easter Bunny Vault Security do allow access to
the vault if you know the right path. For example:

- If your passcode were ihgpwlah, the shortest path would be DDRRRD.

- With kglvqrro, the shortest path would be DDUDRLRRUDRD.

- With ulqzkmiv, the shortest would be DRURDRUDDLLDLUURRDULRLDUUDDDRR.

Given your vault's passcode, what is the shortest path (the actual path,
not just the length) to reach the vault?

--- Part Two ---

You're curious how robust this security solution really is, and so you
decide to find longer and longer paths which still provide access to the
vault. You remember that paths always end the first time they reach the
bottom-right room (that is, they can never pass through it, only end in
it).

For example:

- If your passcode were ihgpwlah, the longest path would take 370  steps.
- With kglvqrro, the longest path would be 492 steps long.
- With ulqzkmiv, the longest path would be 830 steps long.

What is the length of the longest path that reaches the vault?
"""


import hashlib
import sys


def get_data(name):
    f = open(name, 'r')

    return f.read()


def walk(size_x, size_y, code, path, pos_x, pos_y, find_max=False):
    checksum = hashlib.md5(("%s%s" % (code, path)).encode('utf-8')).hexdigest()

    if pos_x == size_x - 1 and pos_y == size_y - 1:
        return path, True

    up, down, left, right = checksum[:4]
    dore_open = ['b', 'c', 'd', 'e', 'f']
    paths = []

    if up in dore_open and pos_y - 1 >= 0:
        path_up, success_up = walk(
            size_x, size_y, code, "%sU" % path, pos_x, pos_y - 1, find_max)

        if success_up:
            paths.append(path_up)
    if down in dore_open and pos_y + 1 < size_y:
        path_down, success_down = walk(
            size_x, size_y, code, "%sD" % path, pos_x, pos_y + 1, find_max)

        if success_down:
            paths.append(path_down)
    if left in dore_open and pos_x - 1 >= 0:
        path_left, success_left = walk(
            size_x, size_y, code, "%sL" % path, pos_x - 1, pos_y, find_max)

        if success_left:
            paths.append(path_left)
    if right in dore_open and pos_x + 1 < size_x:
        path_right, success_right = walk(
            size_x, size_y, code, "%sR" % path, pos_x + 1, pos_y, find_max)

        if success_right:
            paths.append(path_right)

    if len(paths) == 0:
        return path, False
    else:
        lengths = list(map(len, paths))

        if find_max:
            idx = lengths.index(max(lengths))
        else:
            idx = lengths.index(min(lengths))

        return paths[idx], True


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <input_file>" % sys.argv[0])
        sys.exit(1)

    code = get_data(sys.argv[1]).rstrip()

    size_x = 4
    size_y = 4
    pos_x = 0
    pos_y = 0
    path = ''

    path1, success = walk(size_x, size_y, code, path, pos_x, pos_y)
    path2, success = walk(size_x, size_y, code, path, pos_x, pos_y, True)

    print("[Star 1] Shortest path: %s" % path1)
    print("[Star 2] Length of the longest path: %d" % len(path2))


if __name__ == '__main__':
    main()
