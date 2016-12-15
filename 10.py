#!/usr/bin/python

"""
--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing
small microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it
has two microchips, and once it does, it gives each one to a different
bot or puts it in a marked "output" bin. Sometimes, bots take microchips
from "input" bins, too.

Inspecting one of the microchips, it seems like they each contain a
single number; the bots must use some logic to decide what to do with
each chip. You access the local control computer and download the bots'
instructions (your puzzle input).

Some of the instructions specify that a specific-valued microchip should
be given to a specific bot; the rest of the instructions indicate what a
given bot should do with its lower-value or higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2

- Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a
  value-2 chip and a value-5 chip.
- Because bot 2 has two microchips, it gives its lower one (2) to bot 1
  and its higher one (5) to bot 0.
- Then, bot 1 has two microchips; it puts the value-2 chip in output 1  and
  gives the value-3 chip to bot 0.
- Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in
  output 0.

In the end, output bin 0 contains a value-5 microchip, output bin 1
contains a value-2 microchip, and output bin 2 contains a value-3
microchip. In this configuration, bot number 2 is responsible for
comparing value-5 microchips with value-2 microchips.

Based on your instructions, what is the number of the bot that is
responsible for comparing value-61 microchips with value-17 microchips?

--- Part Two ---

What do you get if you multiply together the values of one chip in each
of outputs 0, 1, and 2?
"""


import six
import sys


def get_data(name):
    f = open(name, 'r')

    return f.readlines()


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <input_file>" % sys.argv[0])
        sys.exit(1)

    data = get_data(sys.argv[1])
    entity = {}
    search_for = [17, 61]

    if sys.argv[1].endswith('10_test1.txt'):
        search_for = [2, 5]

    for line in data:
        if line.startswith('value '):
            fields = line.strip().split()
            value = int(fields[1])
            bot = "%s%s" % (fields[4], fields[5])

            if bot not in entity:
                entity[bot] = {
                    'chips': []
                }

            entity[bot]['chips'].append(value)
        elif line.startswith('bot '):
            fields = line.strip().split()
            bot = "%s%s" % (fields[0], fields[1])
            low_to = "%s%s" % (fields[5], fields[6])
            high_to = "%s%s" % (fields[10], fields[11])

            for e in (low_to, high_to):
                if e not in entity:
                    entity[e] = {
                        'chips': []
                    }

            if bot not in entity:
                entity[bot] = {
                    'chips': [],
                    'order': {
                        'low_to': low_to,
                        'high_to': high_to
                    }
                }
            else:
                entity[bot]['order'] = {
                    'low_to': low_to,
                    'high_to': high_to
                }

    has_order = True
    cmp_bot = None

    while has_order:
        has_order = False

        for e, vals in six.iteritems(entity):
            if 'order' in vals:
                has_order = True

                if len(vals['chips']) == 2:
                    if search_for == sorted(vals['chips']):
                        cmp_bot = e.replace('bot', '')

                    if vals['chips'][0] > vals['chips'][1]:
                        entity[vals['order']['low_to']]['chips'].append(
                            vals['chips'].pop())
                        entity[vals['order']['high_to']]['chips'].append(
                            vals['chips'].pop())
                    else:
                        entity[vals['order']['high_to']]['chips'].append(
                            vals['chips'].pop())
                        entity[vals['order']['low_to']]['chips'].append(
                            vals['chips'].pop())

                    del vals['order']

    print("[Star 1] Bot number comparing chip values %d and %d: %s" % (
        search_for[0], search_for[1], cmp_bot))

    multi = 1

    for i in range(3):
        multi *= entity["output%d" % i]['chips'][0]

    print("[Star 2] Multiplied outputs: %d" % multi)


if __name__ == '__main__':
    main()
