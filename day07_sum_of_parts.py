"""
You find yourself standing on a snow-covered coastline; apparently, you landed a little off course. The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher priorities at the moment. You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
Visually, these requirements look like this:



Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

Only C is available, and so it is done first.
Next, both A and F are available. A is first alphabetically, so it is done next.
Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
F is the only choice, so it is done next.
Finally, E is completed.
So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?
"""

from typing import List, Dict, Set, NamedTuple
import re


class Step:
    name: str
    prev_steps: List[str]
    next_steps: List[str]

    def __init__(self, name):
        self.name = name
        self.prev_steps = []
        self.next_steps = []


TEST_CASE = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".split('\n')

PATTERN = re.compile(
    'Step ([A-Z]) must be finished before step ([A-Z]) can begin.')


def get_steps(instructions: List[str]):
    steps = {}
    for instruction in instructions:
        match = re.match(PATTERN, instruction)
        if match:
            name, next_step_name = match.groups()
            try:
                steps[name].next_steps.append(next_step_name)
            except:
                steps[name] = Step(name)
                steps[name].next_steps.append(next_step_name)

            try:
                steps[next_step_name].prev_steps.append(name)
            except:
                steps[next_step_name] = Step(next_step_name)
                steps[next_step_name].prev_steps.append(name)

    return steps


def get_first_step(steps: Dict[str, Step]) -> Dict[str, Step]:
    all_steps = list(steps.values())
    first_steps = {}
    for step in all_steps:
        if step.prev_steps == []:
            first_steps[step.name] = step
    return first_steps


def find_available_step(steps: Dict[str, Step], finished_steps: str):
    sorted_steps = sorted(steps.items(), key = lambda x: x[0])
    for i, sorted_step in sorted_steps:
        if all([prev_step in finished_steps for prev_step in sorted_step.prev_steps]):
            return sorted_step

def process(steps: Dict[str, Step]):
    order = ''
    while len(steps) is not 0:
        candidate = find_available_step(steps, order)
        order += candidate.name
        del steps[candidate.name]
    return order
    

# print(process(get_steps(TEST_CASE)))

with open('models/day07.txt') as f:
    instructions = [line.strip() for line in f.readlines()]
    print(process(get_steps(instructions)))
