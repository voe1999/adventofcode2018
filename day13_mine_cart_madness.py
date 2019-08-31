"""
A crop of this size requires significant logistics to transport produce, soil, fertilizer, and so on. The Elves are very busy pushing things around in carts on some kind of rudimentary system of tracks they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history for another 1000 years, the Elves seem to be making this up as they go along. They haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+). Curves connect exactly two perpendicular pieces of track; for example, this is a closed loop:

/----\
|    |
|    |
\----/
Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left, turning right, or continuing straight. Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/
Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). (On your initial map, the track under each cart is a straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, goes straight the second time, turns right the third time, and then repeats those directions starting again with left the fourth time, straight the fifth time, and so on. This process is independent of the particular intersection at which the cart has arrived - that is, the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a time. They do this based on their current location: carts on the top row move first (acting from left to right), then carts on the second row move (again from left to right), then carts on the third row, and so on. Once each cart has moved one step, the process repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |
First, the top cart moves. It is facing down (v), so it moves down one square. Second, the bottom cart moves. It is facing up (^), so it moves up one square. Because all carts have moved, the first tick ends. Then, the process repeats, starting with the first cart. The first cart moves down, then the second cart moves up - right into the first cart, colliding with it! (The location of the crash is marked with an X.) This ends the second and last tick.

Here is a longer example:

/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/-->\
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/

/---v
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/

/---\
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/

/---\
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/

/---\
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/

/---\
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/---\
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/

/---\
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/

/---\
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/

/---\
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/
After following their respective paths for a while, the carts eventually crash. To help prevent crashes, you'd like to know the location of the first crash. Locations are given in X,Y coordinates, where the furthest left column is X=0 and the furthest top row is Y=0:

           111
 0123456789012
0/---\
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/
In this example, the location of the first crash is 7,3.
"""

import re
from random import random
from typing import Dict, Tuple

TEST_CASE = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
"""

Map = Dict[Tuple[int, int], str]


class Car:
    current_coords: Tuple[int, int]
    facing: str
    last_turn: str
    crashed: bool

    def __init__(self, current_coords, facing):
        self.current_coords = current_coords
        self.facing = facing
        self.last_turn = ''
        self.crashed = False

    def move_one_step(self, traffic_map: Map):
        current_location = traffic_map[self.current_coords]
        x, y = self.current_coords
        if current_location == '|':
            if self.facing == '^':
                self.current_coords = (x, y - 1)
            elif self.facing == 'v':
                self.current_coords = (x, y + 1)
            else:
                raise Exception('car facing error')
        elif current_location == '-':
            if self.facing == '<':
                self.current_coords = (x - 1, y)
            elif self.facing == '>':
                self.current_coords = (x + 1, y)
            else:
                raise Exception('car facing error')
        elif current_location == '/':
            if self.facing == '<':
                self.current_coords = (x, y + 1)
                self.facing = 'v'
            elif self.facing == 'v':
                self.current_coords = (x - 1, y)
                self.facing = '<'
            elif self.facing == '>':
                self.current_coords = (x, y - 1)
                self.facing = '^'
            elif self.facing == '^':
                self.current_coords = (x + 1, y)
                self.facing = '>'
            else:
                raise Exception('car facing error')
        elif current_location == '\\':
            if self.facing == '<':
                self.current_coords = (x, y - 1)
                self.facing = '^'
            elif self.facing == 'v':
                self.current_coords = (x + 1, y)
                self.facing = '>'
            elif self.facing == '>':
                self.current_coords = (x, y + 1)
                self.facing = 'v'
            elif self.facing == '^':
                self.current_coords = (x - 1, y)
                self.facing = '<'
            else:
                raise Exception('car facing error')
        elif current_location == '+':
            if self.last_turn == '' or self.last_turn == 'right':  # turn left
                if self.facing == '<':
                    self.current_coords = (x, y + 1)
                    self.facing = 'v'
                elif self.facing == '>':
                    self.current_coords = (x, y - 1)
                    self.facing = '^'
                elif self.facing == '^':
                    self.current_coords = (x - 1, y)
                    self.facing = '<'
                elif self.facing == 'v':
                    self.current_coords = (x + 1, y)
                    self.facing = '>'
                else:
                    raise Exception('car facing error')
                self.last_turn = 'left'
            elif self.last_turn == 'left':  # straight
                if self.facing == '<':
                    self.current_coords = (x - 1, y)
                elif self.facing == '>':
                    self.current_coords = (x + 1, y)
                elif self.facing == '^':
                    self.current_coords = (x, y - 1)
                elif self.facing == 'v':
                    self.current_coords = (x, y + 1)
                else:
                    raise Exception('car facing error')
                self.last_turn = 'straight'
            elif self.last_turn == 'straight':  # turn right
                if self.facing == '<':
                    self.current_coords = (x, y - 1)
                    self.facing = '^'
                elif self.facing == '>':
                    self.current_coords = (x, y + 1)
                    self.facing = 'v'
                elif self.facing == '^':
                    self.current_coords = (x + 1, y)
                    self.facing = '>'
                elif self.facing == 'v':
                    self.current_coords = (x - 1, y)
                    self.facing = '<'
                else:
                    raise Exception('car facing error')
                self.last_turn = 'right'
        else:
            raise Exception('route tracking error')


Cars = Dict[Tuple[int, int], Car]


def init_map(raw: str) -> Tuple[Map, Cars]:
    lines = raw.split('\n')
    traffic_map: Map = {}
    cars: Cars = {}
    for y, line in enumerate(lines):
        for x, location in enumerate(line):
            match = re.match(r'[|\-/\\+^v<>]', location)
            if match is not None:
                symbol = match.group()[0]
                if symbol == '<' or symbol == '>':
                    traffic_map[(x, y)] = '-'
                    cars[(x, y)] = Car((x, y), symbol)
                elif symbol == '^' or symbol == 'v':
                    traffic_map[(x, y)] = '|'
                    cars[(x, y)] = Car((x, y), symbol)
                else:
                    traffic_map[(x, y)] = symbol
    return traffic_map, cars


def main():
    with open('models/day13.txt', 'r') as f:
        RAW = f.read()
    traffic_map, cars = init_map(RAW)
    collided = False
    turns = 0
    while not collided:
        cars_coords = set()
        for car in cars.values():
            car.move_one_step(traffic_map)
            if car.current_coords not in cars_coords:
                cars_coords.add(car.current_coords)
            else:
                print(car.current_coords)
                return
        turns += 1


# main()

def main2():
    TEST_CASE2 = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""
    with open('models/day13.txt', 'r') as f:
        RAW2 = f.read()
    traffic_map, cars = init_map(TEST_CASE2)
    car_ids = {(k + 1): v[1] for k, v in enumerate(sorted(cars.items(), key=lambda x: x[1].current_coords))}

    while len([good_car for good_car in car_ids.values() if good_car.crashed is False]) > 1:
        cars_coords = set([car.current_coords for car in car_ids.values() if car.crashed is False])
        # print(cars_coords)
        for car_id, car in car_ids.items():
            if car.crashed is True:
                continue
            cars_coords.remove(car.current_coords)
            car.move_one_step(traffic_map)

            if car.current_coords not in cars_coords:
                cars_coords.add(car.current_coords)
            else:
                car_ids[car_id].crashed = True
                for other_id, other_car in car_ids.items():
                    if other_car.current_coords == car.current_coords and car_id != other_id:
                        # print(car, other_car)
                        car_ids[other_id].crashed = True
                print('crashed at ', car.current_coords)

    return [good_car for good_car in car_ids.values() if good_car.crashed is False][0].__dict__


print(main2())
