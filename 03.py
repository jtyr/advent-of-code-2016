#!/usr/bin/python

"""
--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of
hallways and office furniture that makes up this part of Easter Bunny HQ.
This must be a graphic design department; the walls are covered in
specifications for triangles.

Or are they?

The design document gives the side lengths of each triangle it describes,
but... 5 10 25? Some of these aren't triangles. You can't help but mark
the impossible ones.

In a valid triangle, the sum of any two sides must be larger than the
remaining side. For example, the "triangle" given above is impossible,
because 5 + 10 is not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to
you that triangles are specified in groups of three vertically. Each set
of three numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same
hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns, how many of the
listed triangles are possible?
"""


def get_data():
    f = open("input/03.txt", "r")

    return f.readlines()


def is_triangle(a, b, c):
    if (
            a + b > c and
            b + c > a and
            c + a > b):
        return True

    return False


def main():
    data = get_data()
    cnt1 = 0
    cnt2 = 0
    lst1 = []
    lst2 = []
    lst3 = []

    for line in data:
        a, b, c = map(int, line.split())

        lst1.append(a)
        lst2.append(b)
        lst3.append(c)

        cnt1 += is_triangle(a, b, c)

    sides = []

    for item in lst1 + lst2 + lst3:
        sides.append(item)

        if len(sides) == 3:
            cnt2 += is_triangle(*sides)
            sides = []

    print("[Star 1] Count: %d" % cnt1)
    print("[Star 2] Count: %d" % cnt2)


if __name__ == '__main__':
    main()
