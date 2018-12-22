from typing import List, Iterator

with open('../models/day01.txt') as f:
    numbers = [int(line.strip()) for line in f]


def all_frequencies(numbers: List[int], start: int = 0) -> Iterator[int]:
    frequency = 0

    while True:
        for number in numbers:
            yield frequency
            frequency += number


def first_repeat_frequency(numbers: List[int], start: int = 0) -> int:
    seen = set()

    for frequency in all_frequencies(numbers, start):
        if frequency in seen:
            return frequency
        else:
            seen.add(frequency)


assert first_repeat_frequency([1, -1]) == 0

print(first_repeat_frequency(numbers))
