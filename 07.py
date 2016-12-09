#!/usr/bin/python

"""
--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP
addresses (they're IPv7, of course; IPv6 is much too limited). You'd like
to figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or
ABBA. An ABBA is any four-character sequence which consists of a pair of
two different characters followed by the reverse of that pair, such as
xyyx  or abba. However, the IP also must not have an ABBA within any
hypernet sequences, which are contained by square brackets.

For example:

- abba[mnop]qrst supports TLS (abba outside square brackets).
- abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even
  though xyyx is outside square brackets).
- aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior
  characters must be different).
- ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even
  though it's within a larger string).

How many IPs in your puzzle input support TLS?

--- Part Two ---

You would also like to know which IPs support SSL (super-secret
listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere
in the supernet sequences (outside any square bracketed sections), and a
corresponding Byte Allocation Block, or BAB, anywhere in the hypernet
sequences. An ABA is any three-character sequence which consists of the
same character twice with a different character between them, such as xyx
or aba. A corresponding BAB is the same characters but in reversed
positions: yxy and bab, respectively.

For example:

- aba[bab]xyz supports SSL (aba outside square brackets with corresponding
  bab within square brackets).
- xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
- aaa[kek]eke supports SSL (eke in supernet with corresponding kek in
  hypernet; the aaa sequence is not related, because the interior character
  must be different).
- zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a
  corresponding bzb, even though zaz and zbz overlap).

How many IPs in your puzzle input support SSL?
"""


import sys


def get_data(name):
    f = open(name, 'r')

    return f.readlines()


def is_symmetric(s):
    if len(s) == 3:
        if s[0] == s[2] and s[1] != s[0]:
            return True
    if len(s) == 4:
        if s[:2] == s[:1:-1] and s[:2] != s[2:]:
            return True

    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <input_file>" % sys.argv[0])
        sys.exit(1)

    data = get_data(sys.argv[1])
    cnt1 = 0
    cnt2 = 0
    size1 = 4
    size2 = 3
    msgs = []

    for line in data:
        all_pairs = line.strip().split(']')

        record = {
            'inside': [],
            'outside': []
        }

        for pair in all_pairs:
            split_pair = pair.split('[')
            inside = None

            if len(split_pair) == 1:
                record['outside'].append(split_pair[0])
            else:
                record['outside'].append(split_pair[0])
                record['inside'].append(split_pair[1])

        msgs.append(record)

    for msg in msgs:
        outside_valid = False
        inside_valid = False
        ssl_valid = False

        for outside in msg['outside']:
            for n in range(len(outside)-size1+1):
                if is_symmetric(outside[n:n+size1]):
                    outside_valid = True
                    break

            if outside_valid:
                break

        for inside in msg['inside']:
            if inside is not None:
                for n in range(len(inside)-size1+1):
                    if is_symmetric(inside[n:n+size1]):
                        inside_valid = True
                        break

            if inside_valid:
                break

        if outside_valid and not inside_valid:
            cnt1 += 1

        for outside in msg['outside']:
            for n in range(len(outside)-size2+1):
                s = outside[n:n+size2]

                if is_symmetric(s):
                    inverted = "%s%s%s" % (s[1], s[0], s[1])

                    for inside in msg['inside']:
                        if inverted in inside:
                            ssl_valid = True
                            break

                if ssl_valid:
                    break

            if ssl_valid:
                break

        if ssl_valid:
            cnt2 += 1

    print("[Star 1] Count: %s" % cnt1)
    print("[Star 2] Count: %s" % cnt2)


if __name__ == '__main__':
    main()
