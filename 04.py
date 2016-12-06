#!/usr/bin/python

"""
--- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms. Of
course, the list is encrypted and full of decoy data, but the
instructions to decode the list are barely hidden nearby. Better remove
the decoy data first.

Each room consists of an encrypted name (lowercase letters separated by
dashes) followed by a dash, a sector ID, and a checksum in square
brackets.

A room is real (not a decoy) if the checksum is the five most common
letters in the encrypted name, in order, with ties broken by
alphabetization. For example:

- aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters
  are a (5), b (3), and then a tie between x, y, and z, which are listed
  alphabetically.
- a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters
  are all tied (1 of each), the first five are listed alphabetically.
- not-a-real-room-404[oarel] is a real room.
- totally-real-room-200[decoy] is not.

Of the real rooms from the list above, the sum of their sector IDs is 1514.

What is the sum of the sector IDs of the real rooms?

--- Part Two ---

With all the decoy data out of the way, it's time to decrypt this list
and get moving.

The room names are encrypted by a state-of-the-art shift cipher, which is
nearly unbreakable without the right software. However, the information
kiosk designers at Easter Bunny HQ were not expecting to deal with a
master cryptographer like yourself.

To decrypt a room name, rotate each letter forward through the alphabet a
number of times equal to the room's sector ID. A becomes B, B becomes C,
Z  becomes A, and so on. Dashes become spaces.

For example, the real name for qzmt-zixmtkozy-ivhz-343 is "very encrypted
name".

What is the sector ID of the room where North Pole objects are stored?
"""


import re
import sys


def get_data(name):
    f = open(name, 'r')

    return f.readlines()


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <input_file>" % sys.argv[0])
        sys.exit(1)

    data = get_data(sys.argv[1])
    sector_sum = 0
    storage_id = 0

    for line in data:
        m = re.search('^(.+)-(\d+)\[(.+)\]$', line.strip())
        name = m.group(1)
        sector_id = int(m.group(2))
        checksum = m.group(3)
        occurrences = {}

        for ch in name:
            if ch != '-':
                if ch in occurrences:
                    occurrences[ch] += 1
                else:
                    occurrences[ch] = 1

        sorted_items = sorted(
            occurrences.items(), key=lambda x: (-x[1], x[0]))
        valid = True

        for i, ch in enumerate(checksum):
            if ch != sorted_items[i][0]:
                valid = False

                break

        if valid:
            sector_sum += sector_id

        s_name = ''

        for ch in name:
            for n in range(sector_id):
                if ch == '-':
                    ch = ' '

                    break
                else:
                    if ch == 'z':
                        ch = '`'

                ch = chr(ord(ch) + 1)

            s_name += ch

        if s_name == 'northpole object storage':
            storage_id = sector_id

    print("[Star 1] Sum: %d" % sector_sum)
    print("[Star 2] Sector ID: %d" % storage_id)


if __name__ == '__main__':
    main()
