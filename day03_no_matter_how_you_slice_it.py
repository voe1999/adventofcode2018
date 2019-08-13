"""
The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........
The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?
"""
from typing import List, Optional

with open('models/day03.txt') as f:
    claims = [line.strip() for line in f.readlines()]


class Rectangle():
    top_left_x: int
    top_left_y: int
    top_right_x: int
    top_right_y: int
    bottom_left_x: int
    bottom_left_y: int
    bottom_right_x: int
    bottom_right_y: int

    def __init__(self, x: int, y: int, width: int, height: int):
        self.top_left_x = x
        self.top_left_y = y
        self.top_right_x = x + width
        self.top_right_y = y
        self.bottom_left_x = x
        self.bottom_left_y = y + height
        self.bottom_right_x = x + width
        self.bottom_right_y = y + height


def get_rectangles_from_claims(claims: List[str]) -> List[Rectangle]:
    recs = []
    for claim in claims:
        x = int(claim.split('@ ')[1].split(',')[0])
        y = int(claim.split('@ ')[1].split(',')[1].split(':')[0])
        width = int(claim.split('@ ')[1].split(
            ',')[1].split(':')[1].split('x')[0])
        height = int(claim.split('@ ')[1].split(
            ',')[1].split(':')[1].split('x')[1])
        recs.append(Rectangle(x, y, width, height))
    return recs


def get_overlap_rec(rec1: Rectangle, rec2: Rectangle) -> Optional[Rectangle]:
   
    overlap_width = (rec1.bottom_right_x - rec1.bottom_left_x) + (rec2.bottom_right_x - rec2.bottom_left_x) - (max(rec1.bottom_right_x, rec2.bottom_right_x) - min(rec1.bottom_left_x, rec2.bottom_left_x))
    overlap_height = (rec1.top_left_y - rec1.bottom_left_y) + (rec2.top_left_y - rec2.bottom_left_y) - (max(rec1.top_left_y, rec2.top_left_y) - min(rec1.bottom_left_y, rec2.bottom_left_y))

    if overlap_width > 0 & overlap_height > 0:
        x = max(rec1.top_left_x, rec2.top_left_x)
        y = max(rec1.top_left_y, rec2.top_left_y)
        return Rectangle(x, y, overlap_width, overlap_height)

def test():
    recs = get_rectangles_from_claims(claims)
    for i in range(len(recs)):
        for j in range(i + 1, len(recs)):
            print(get_overlap_rec(recs[i], recs[j]))
        
test()
print('done')
# n2
def get_overlap_recs(all_recs: List[Rectangle]) -> List[Rectangle]:
    overlap_recs = all_recs
    for i in range(len(all_recs)):
        for j in range(i + 1, len(overlap_recs)):
            overlap_rec = get_overlap_rec(overlap_recs[i], overlap_recs[j])
            if overlap_rec == None:
                continue
            else:
                overlap_recs.remove(overlap_recs[j])
                overlap_recs[i] = overlap_rec
                continue
    return overlap_recs


def get_all_overlap_area(overlap_recs: List[Rectangle]) -> int:
    return
