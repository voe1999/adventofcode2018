"""
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?
"""

from typing import NamedTuple, List, Set

from collections import Counter

TEST_CASE = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""".split('\n')

class Location(NamedTuple):
    x: int
    y: int


class Candidate(NamedTuple):
    x: int
    y: int
    area: int
    locations: List[Location]

    @classmethod
    def get_area(self):
        self.area = len(self.locations)
        return self.area


def get_original_candidates(locations: List[str]):
    candidates: List[Candidate] = []
    for location in locations:
        x, y = [int(coord) for coord in location.split(', ')]
        candidates.append(Candidate(x, y, 0, []))
    return candidates

def get_max_xy(candidates: List[Candidate]) -> Set[int]:
    xs: List[int] = []
    ys: List[int] = []
    ret = set()
    for candidate in candidates:
        xs.append(candidate.x)
        ys.append(candidate.y)
    ret.add(max(xs))
    ret.add(max(ys))
    return ret

def get_all_locations(max_x: int, max_y: int) -> List[Location]:
    locations: List[Location] = []
    for x in range(max_x + 3):
        for y in range(max_y + 3):
            locations.append(Location(x, y))
    return locations     

def calculate_manhattan_distance(l1: Location, l2: Candidate) -> int:
    return abs(l1.x - l2.x) + abs(l1.y - l2.y)

def set_locations_to_candidate(locations: List[Location], candidates: List[Candidate]) -> int:
    for location in locations:
        distances: Counter = Counter()
        for candidate in candidates:
            distances[candidate] = calculate_manhattan_distance(location, candidate)
        biggest_two = distances.most_common(2)
        if biggest_two[0] > biggest_two[1]:
            print(biggest_two)
            # biggest_two[0][0].locations.append(location)
    areas = []
    for candidate in candidates:
        areas.append(candidate.get_area())
    return max(areas)

candidates = get_original_candidates(TEST_CASE)
max_x, max_y = get_max_xy(candidates)
locations = get_all_locations(max_x, max_y)

print(set_locations_to_candidate(locations, candidates))