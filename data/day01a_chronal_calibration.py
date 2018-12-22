with open('../models/day01.txt') as f:
    numbers = [int(line.strip()) for line in f]

print(sum(numbers))
