"""
The year 518 is significantly more underground than your history books implied. Either that, or you've arrived in a vast cavern network under the North Pole.

After exploring a little, you discover a long tunnel that contains a row of small pots as far as you can see to your left and right. A few of them contain plants - someone is trying to grow things in these geothermally-heated caves.

The pots are numbered, with 0 in front of you. To the left, the pots are numbered -1, -2, -3, and so on; to the right, 1, 2, 3.... Your puzzle input contains a list of pots from 0 to the right and whether they do (#) or do not (.) currently contain a plant, the initial state. (No other pots currently contain plants.) For example, an initial state of #..##.... indicates that pots 0, 3, and 4 currently contain plants.

Your puzzle input also contains some notes you find on a nearby table: someone has been trying to figure out how these plants spread to nearby pots. Based on the notes, for each generation of plants, a given pot has or does not have a plant based on whether that pot (and the two pots on either side of it) had a plant in the last generation. These are written as LLCRR => N, where L are pots to the left, C is the current pot being considered, R are the pots to the right, and N is whether the current pot will have a plant in the next generation. For example:

A note like ..#.. => . means that a pot that contains a plant but with no plants within two pots of it will not have a plant in it during the next generation.
A note like ##.## => . means that an empty pot with two plants on each side of it will remain empty in the next generation.
A note like .##.# => # means that a pot has a plant in a given generation if, in the previous generation, there were plants in that pot, the one immediately to the left, and the one two pots to the right, but not in the ones immediately to the right and two to the left.
It's not clear what these plants are for, but you're sure it's important, so you'd like to make sure the current configuration of plants is sustainable by determining what will happen after 20 generations.

For example, given the following input:

initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
For brevity, in this example, only the combinations which do produce a plant are listed. (Your input includes all possible combinations.) Then, the next 20 generations will look like this:

                 1         2         3     
       0         0         0         0     
 0: ...#..#.#..##......###...###...........
 1: ...#...#....#.....#..#..#..#...........
 2: ...##..##...##....#..#..#..##..........
 3: ..#.#...#..#.#....#..#..#...#..........
 4: ...#.#..#...#.#...#..#..##..##.........
 5: ....#...##...#.#..#..#...#...#.........
 6: ....##.#.#....#...#..##..##..##........
 7: ...#..###.#...##..#...#...#...#........
 8: ...#....##.#.#.#..##..##..##..##.......
 9: ...##..#..#####....#...#...#...#.......
10: ..#.#..#...#.##....##..##..##..##......
11: ...#...##...#.#...#.#...#...#...#......
12: ...##.#.#....#.#...#.#..##..##..##.....
13: ..#..###.#....#.#...#....#...#...#.....
14: ..#....##.#....#.#..##...##..##..##....
15: ..##..#..#.#....#....#..#.#...#...#....
16: .#.#..#...#.#...##...#...#.#..##..##...
17: ..#...##...#.#.#.#...##...#....#...#...
18: ..##.#.#....#####.#.#.#...##...##..##..
19: .#..###.#..#.#.#######.#.#.#..#.#...#..
20: .#....##....#####...#######....#.#..##.
The generation is shown along the left, where 0 is the initial state. The pot numbers are shown along the top, where 0 labels the center pot, negative-numbered pots extend to the left, and positive pots extend toward the right. Remember, the initial state begins at pot 0, which is not the leftmost pot used in this example.

After one generation, only seven plants remain. The one in pot 0 matched the rule looking for ..#.., the one in pot 4 matched the rule looking for .#.#., pot 9 matched .##.., and so on.

In this example, after 20 generations, the pots shown as # contain plants, the furthest left of which is pot -2, and the furthest right of which is pot 34. Adding up all the numbers of plant-containing pots after the 20th generation produces 325.

After 20 generations, what is the sum of the numbers of all pots which contain a plant?
"""

TEST_CASE = '#..#.#..##......###...###'

TEST_PATTERN = """...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""

import re
from typing import Dict, List


def get_initial_state(input: str) -> List[str]:
    return list(input)


Predictions = Dict[str, str]


def prepare_predictions(input: str) -> Predictions:
    patterns = input.split('\n')
    predictions: Predictions = {}
    for pattern in patterns:
        combo, prediction = re.match(r'(.*) => (.)', pattern).groups()
        predictions[combo] = prediction
    return predictions


def predict(generations: int, initial_state: List[str], predictions: Predictions):
    # negative-numbered pots, with index of "i"
    left_part = list('.......................................................')
    # positive-numbered pots, which is 'initial_state', with index of 'j'
    right_part = initial_state.copy()
    # when predicting, concatenate the two lists
    # pot_number = i if pot_number >= 0
    # pot_number = j if pot_number < 0
    for _ in range(generations):
        left_part.insert(0, '.')
        left_part.insert(0, '.')
        left_part.insert(0, '.')
        right_part.append('.')
        right_part.append('.')
        right_part.append('.')

        next_left_part = left_part.copy()
        next_right_part = right_part.copy()

        for i in range(2, len(left_part + right_part) - 2):
            pot_number = i - len(left_part)
            pot_left_1 = pot_number - 2
            pot_left_2 = pot_number - 1
            pot_right_1 = pot_number + 1
            pot_right_2 = pot_number + 2

            plant1 = right_part[pot_left_1] if pot_left_1 >= 0 else left_part[pot_left_1]
            plant2 = right_part[pot_left_2] if pot_left_2 >= 0 else left_part[pot_left_2]
            plant3 = right_part[pot_number] if pot_number >= 0 else left_part[pot_number]
            plant4 = right_part[pot_right_1] if pot_right_1 >= 0 else left_part[pot_right_1]
            plant5 = right_part[pot_right_2] if pot_right_2 >= 0 else left_part[pot_right_2]

            plants = plant1 + plant2 + plant3 + plant4 + plant5

            try:
                prediction = predictions[plants]
            except:
                prediction = '.'

            if pot_number >= 0:
                next_right_part[pot_number] = prediction
            else:
                next_left_part[pot_number] = prediction

        left_part = next_left_part
        right_part = next_right_part

        left_sum = sum([(i - len(left_part)) for i, c in enumerate(left_part) if c == '#'])
        right_sum = sum([i for i, c in enumerate(right_part) if c == '#'])

    # return ''.join(plant for plant in (left_part + right_part))
    return left_sum + right_sum


assert predict(20, get_initial_state(TEST_CASE), prepare_predictions(TEST_PATTERN)) == 325

INPUT_CASE = '#...#..##.......####.#..###..#.##..########.#.#...#.#...###.#..###.###.#.#..#...#.#..##..#######.##'
INPUT_PATTERN = """#..#. => #
#.#.. => #
###.. => #
##..# => .
.#.## => #
..... => .
...#. => #
##.#. => #
#.#.# => .
###.# => #
....# => .
####. => #
.##.. => #
#.##. => #
#..## => #
##... => #
#...# => .
##.## => #
.#... => .
.#..# => #
..#.# => #
##### => .
.#### => #
..#.. => #
#.### => .
..##. => .
.##.# => #
.#.#. => .
..### => .
.###. => .
...## => .
#.... => ."""

print(predict(20, get_initial_state(INPUT_CASE), prepare_predictions(INPUT_PATTERN)))
