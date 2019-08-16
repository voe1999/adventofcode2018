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


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
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

from typing import List, Dict, Set
import re, random
from collections import Counter

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

PATTERN = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin.')

def get_steps(instructions: List[str]):
    steps: Dict[str, Step] = {}
    for instruction in instructions:
        name, next_step_name = re.match(PATTERN, instruction).groups()
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


def get_first_step(steps: Dict[str, Step]):
    random_step = list(steps.values())[random.randint(0, len(steps.keys()) - 1)]
    while random_step.prev_steps != []:
        step_name = random_step.prev_steps[random.randint(0, len(random_step.prev_steps) - 1)]
        random_step = steps[step_name]
    return random_step

def process(steps: Dict[str, Step]) -> str:
    order = ''
    current_step = get_first_step(steps)
    available_steps = set()
    available_steps.add(current_step.name)
    while True:
        next_try_step, order, available_steps = try_make_a_step(current_step, order, available_steps, steps)
        if next_try_step is None:
            break
        else:
            current_step = next_try_step
       
    return order 

def try_make_a_step(step: Step, executed_steps: str, available_steps: Set[str], steps: Dict[str, Step]):
    try_step = step
    while not all([prev_step in executed_steps for prev_step in try_step.prev_steps]):
       not_completed_steps = [prev_step for prev_step in try_step.prev_steps if prev_step not in executed_steps]
       try_step = steps[not_completed_steps[0]]

    executed_steps += try_step.name
    available_steps.add(try_step.name)
    available_steps.update(try_step.next_steps)
    available_steps.remove(try_step.name)
    try:
        next_try_step = steps[sorted(available_steps)[0]]
        return next_try_step, executed_steps, available_steps
    except:
        return None, executed_steps, available_steps

def get_step_names(ins: List[str]) -> Set[str]:
    s = set()
    for i in ins:
        name, next_step_name = re.match(PATTERN, i).groups()
        s.add(name)
        s.add(next_step_name)
    return s

# print(process(get_steps(TEST_CASE)))

with open('models/day07.txt') as f:
    instructions = [line.strip() for line in f.readlines()]
    string = process(get_steps(instructions))
    print(string)

