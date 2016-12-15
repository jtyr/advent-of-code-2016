#!/usr/bin/python

"""
--- Day 14: One-Time Pad ---

In order to communicate securely with Santa while you're on this mission,
you've been using a one-time pad that you generate using a pre-agreed
algorithm. Unfortunately, you've run out of keys in your one-time pad,
and so you need to generate some more.

To generate keys, you first get a stream of random data by taking the MD5
of a pre-arranged salt (your puzzle input) and an increasing integer
index (starting with 0, and represented in decimal); the resulting MD5
hash should be represented as a string of lowercase hexadecimal digits.

However, not all of these MD5 hashes are keys, and you need 64 new keys
for your one-time pad. A hash is a key only if:

- It contains three of the same character in a row, like 777. Only
  consider the first such triplet in a hash.

- One of the next 1000 hashes in the stream contains that same character
  five times in a row, like 77777.

Considering future hashes for five-of-a-kind sequences does not cause
those hashes to be skipped; instead, regardless of whether the current
hash is a key, always resume testing for keys starting with the very next
hash.

For example, if the pre-arranged salt is abc:

- The first index which produces a triple is 18, because the MD5 hash of
  abc18 contains ...cc38887a5.... However, index 18 does not count as a key
  for your one-time pad, because none of the next thousand hashes (index 19
  through index 1018) contain 88888.

- The next index which produces a triple is 39; the hash of abc39
  contains eee. It is also the first key: one of the next thousand hashes
  (the one at index 816) contains eeeee.

- None of the next six triples are keys, but the one after that, at index
  92, is: it contains 999 and index 200 contains 99999.

- Eventually, index 22728 meets all of the criteria to generate the 64th
key.

So, using our example salt of abc, index 22728 produces the 64th key.

Given the actual salt in your puzzle input, what index produces your 64th
one-time pad key?

--- Part Two ---

Of course, in order to make this process even more secure, you've also
implemented key stretching.

Key stretching forces attackers to spend more time generating hashes.
Unfortunately, it forces everyone else to spend more time, too.

To implement key stretching, whenever you generate a hash, before you use
it, you first find the MD5 hash of that hash, then the MD5 hash of that
hash, and so on, a total of 2016 additional hashings. Always use
lowercase hexadecimal representations of hashes.

For example, to find the stretched hash for index 0 and salt abc:

- Find the MD5 hash of abc0: 577571be4de9dcce85a041ba0410f29f.
- Then, find the MD5 hash of that hash: eec80a0c92dc8a0777c619d9bb51e910.
- Then, find the MD5 hash of that hash: 16062ce768787384c81fe17a7a60c7e3.
- ...repeat many times...
- Then, find the MD5 hash of that hash: a107ff634856bb300138cac6568c0f24.

So, the stretched hash for index 0 in this situation is a107ff.... In the
end, you find the original hash (one use of MD5), then find the
hash-of-the-previous-hash 2016 times, for a total of 2017 uses of MD5.

The rest of the process remains the same, but now the keys are entirely
different. Again for salt abc:

- The first triple (222, at index 5) has no matching 22222 in the next
  thousand hashes.
- The second triple (eee, at index 10) hash a matching eeeee at index 89,
  and so it is the first key.
- Eventually, index 22551 produces the 64th key (triple fff with matching
  fffff at index 22859.

Given the actual salt in your puzzle input and using 2016 extra MD5 calls
of key stretching, what index now produces your 64th one-time pad key?
"""


import hashlib
import sys


def get_data(name):
    f = open(name, 'r')

    return f.read()


def get_hash(s, strech):
    checksum = hashlib.md5(s.encode('utf-8')).hexdigest()

    if strech:
        for n in range(2016):
            checksum = hashlib.md5(checksum.encode('utf-8')).hexdigest()

    return checksum


def find_key(salt, idx, cand, keys, strech=False):
    checksum = get_hash("%s%d" % (salt, idx), strech)

    cnt = 0

    # Hash has triplet?
    for i in range(1, 32):
        if checksum[i] == checksum[i-1]:
            cnt += 1
        else:
            cnt = 0

        if cnt == 2:
            record = {
                'index': idx,
                'ch': checksum[i],
                'checksum': checksum,
                'distance': 1,
                'run': True
            }

            cand.append(record)

            break

    for c in cand:
        if c['run'] and c['checksum'] != checksum and len(keys) < 64:
            if c['ch'] * 5 in checksum:
                keys.append(dict(c))
                keys[-1]['match'] = checksum
                c['run'] = False
            else:
                c['distance'] += 1

                if c['distance'] == 1000:
                    c['run'] = False


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <input_file>" % sys.argv[0])
        sys.exit(1)

    salt = get_data(sys.argv[1]).strip()
    keys1 = []
    cand = []
    idx = 0

    while len(keys1) < 64:
        find_key(salt, idx, cand, keys1)
        idx += 1

    print("[Star 1] Index of 64th key: %d" % keys1[-1]['index'])

    keys2 = []
    cand = []
    idx = 0

    while len(keys2) < 64:
        find_key(salt, idx, cand, keys2, True)
        idx += 1

    print("[Star 2] Index of 64th key: %d" % keys2[-1]['index'])


if __name__ == '__main__':
    main()
