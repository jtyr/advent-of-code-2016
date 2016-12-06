#!/usr/bin/python

"""
--- Day 6: Signals and Noise ---

Something is jamming your communications with Santa. Fortunately, your
signal is only partially jammed, and protocol in situations like this is
to switch to a simple repetition code to get the message through.

In this model, the same message is sent repeatedly. You've recorded the
repeating message signal (your puzzle input), but the data seems quite
corrupted - almost too badly to recover. Almost.

All you need to do is figure out which character is most frequent for
each position. For example, suppose you had recorded the following
messages:

eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar

The most common character in the first column is e; in the second, a; in
the third, s, and so on. Combining these characters returns the
error-corrected message, easter.

Given the recording in your puzzle input, what is the error-corrected
version of the message being sent?

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

Of course, that would be the message - if you hadn't agreed to use a
modified repetition code instead.

In this modified code, the sender instead transmits what looks like
random data, but for each character, the character they actually want to
send is slightly less likely than the others. Even after signal-jamming
noise, you can look at the letter distributions in each column and choose
the least common letter to reconstruct the original message.

In the above example, the least common character in the first column is
a; in the second, d, and so on. Repeating this process for the remaining
characters produces the original message, advent.

Given the recording in your puzzle input and this new decoding
methodology, what is the original message that Santa is trying to send?
"""


import sys


def get_data(name):
    f = open(name, 'r')

    return f.readlines()


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <input_file>" % sys.argv[0])
        sys.exit(1)

    data = get_data(sys.argv[1])
    occurrences = ({}, {}, {}, {}, {}, {}, {}, {})
    message1 = ''
    message2 = ''

    for line in data:
        line = line.strip()

        for i, ch in enumerate(line):
            if ch in occurrences[i]:
                occurrences[i][ch] += 1
            else:
                occurrences[i][ch] = 1

    for col in occurrences:
        if len(col):
            sorted_items = sorted(col.items(), key=lambda x: x[1])
            message1 += sorted_items[-1][0]
            message2 += sorted_items[0][0]

    print("[Star 1] Message: %s" % message1)
    print("[Star 2] Message: %s" % message2)


if __name__ == '__main__':
    main()
