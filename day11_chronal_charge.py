"""
You watch the Elves and their sleigh fade into the distance as they head toward the North Pole.

Actually, you're the one fading. The falling sensation returns.

The low fuel warning light is illuminated on your wrist-mounted device. Tapping it once causes it to project a hologram of the situation: a 300x300 grid of fuel cells and their current power levels, some negative. You're not sure what negative power means in the context of time travel, but it can't be good.

Each fuel cell has a coordinate ranging from 1 to 300 in both the X (horizontal) and Y (vertical) direction. In X,Y notation, the top-left cell is 1,1, and the top-right cell is 300,1.

The interface lets you select any 3x3 square of fuel cells. To increase your chances of getting to your destination, you decide to choose the 3x3 square with the largest total power.

The power level in a given fuel cell can be found through the following process:

Find the fuel cell's rack ID, which is its X coordinate plus 10.
Begin with a power level of the rack ID times the Y coordinate.
Increase the power level by the value of the grid serial number (your puzzle input).
Set the power level to itself multiplied by the rack ID.
Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
Subtract 5 from the power level.
For example, to find the power level of the fuel cell at 3,5 in a grid with serial number 8:


The rack ID is 3 + 10 = 13.
The power level starts at 13 * 5 = 65.
Adding the serial number produces 65 + 8 = 73.
Multiplying by the rack ID produces 73 * 13 = 949.
The hundreds digit of 949 is 9.
Subtracting 5 produces 9 - 5 = 4.
So, the power level of this fuel cell is 4.

Here are some more example power levels:

Fuel cell at  122,79, grid serial number 57: power level -5.
Fuel cell at 217,196, grid serial number 39: power level  0.
Fuel cell at 101,153, grid serial number 71: power level  4.
Your goal is to find the 3x3 square which has the largest total power. The square must be entirely within the 300x300 grid. Identify this square using the X,Y coordinate of its top-left fuel cell. For example:

For grid serial number 18, the largest total 3x3 square has a top-left corner of 33,45 (with a total power of 29); these fuel cells appear in the middle of this 5x5 region:

-2  -4   4   4   4
-4   4   4   4  -5
 4   3   3   4  -4
 1   1   2   4  -3
-1   0   2  -5  -2
For grid serial number 42, the largest 3x3 square's top-left is 21,61 (with a total power of 30); they are in the middle of this region:

-3   4   2   2   2
-4   4   3   3   4
-5   3   3   4  -4
 4   3   3   4  -3
 3   3   3  -5  -1
What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest total power?
"""

from typing import List

class Cell:
    x: int
    y: int
    power_level: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_power_level(self, serial_number: int):
        rack_id = self.x + 10
        power_level = self.y * rack_id
        power_level += serial_number
        power_level *= rack_id

        digits = str(power_level)
        if len(digits) <= 2:
            hundreds_digit = 0
        else:
            hundreds_digit = int(digits[-3])
        power_level = hundreds_digit
        power_level -= 5
        return power_level

assert Cell(3,5).get_power_level(8) == 4
assert Cell(122,79).get_power_level(57) == -5
assert Cell(217,196).get_power_level(39) == 0
assert Cell(101,153).get_power_level(71) == 4


class Square:
    x: int
    y: int
    children: List[Cell]
    total_power_level: int

    def __init__(self, x: int, y: int, size: int):
        MAX_X = 300
        MAX_Y = 300
        self.children = []

        for cx in range(x, x+size):
            for cy in range(y, y+size):
                if cx > MAX_X or cy > MAX_Y:
                    self.children.clear()
                    raise Exception('exceeded range')

                self.children.append(Cell(cx, cy))

        self.x = x
        self.y = y

    def get_total_power_level(self, serial_number: int):
        sum = 0
        for child in self.children:
            sum += child.get_power_level(serial_number)
        return sum

# print([s.__dict__ for s in Square(112,5).children])

# assert Square(33,45).get_total_power_level(18) == 29
# assert Square(21,61).get_total_power_level(42) == 30

def find_powerest_square(serial_number: int):

    powers = {}

    for x in range(1, 300 + 1):
        for y in range(1, 300 + 1):
            for size in range(1, 300 - max(x, y) + 1):
                try:
                    power_level = Square(x, y, size).get_total_power_level(serial_number)
                    powers[(x, y)] = power_level
                except:
                    continue

    sorted_powers = sorted(powers.items(), key=lambda x: x[1], reverse=True)
    return sorted_powers[0][0]

# assert find_powerest_square(18) == (33,45)
# assert find_powerest_square(42) == (21,61)

# print(find_powerest_square(9810))

"""
You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3. Sizes from 1x1 to 300x300 are supported.

Realizing this, you now must find the square of any size with the largest total power. Identify this square by including its size as a third parameter after the top-left coordinate: a 9x9 square with a top-left corner of 3,5 is identified as 3,5,9.

For example:

For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner of 90,269, so its identifier is 90,269,16.
For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner of 232,251, so its identifier is 232,251,12.
What is the X,Y,size identifier of the square with the largest total power?
"""

assert find_powerest_square(18) == (90,269,16)
