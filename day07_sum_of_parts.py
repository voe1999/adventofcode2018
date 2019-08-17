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

from typing import List, Dict, Set, Tuple
import re


class Step:
    name: str
    prev_steps: List[str]
    next_steps: List[str]
    finish_time: int

    def __init__(self, name):
        self.name = name
        self.prev_steps = []
        self.next_steps = []
        self.finish_time = 99999


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
    steps: Dict[str, Step] = {}
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


def find_available_step(steps: Dict[str, Step], finished_steps: str):
    sorted_steps = sorted(steps.items(), key=lambda x: x[0])
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

# with open('models/day07.txt') as f:
#     instructions = [line.strip() for line in f.readlines()]
#     print(process(get_steps(instructions)))


"""
As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .        
   1        C          .        
   2        C          .        
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE
Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
"""


def work(steps: Dict[str, Step]):
    all_steps = steps.copy()
    current_time = 0
    unfinished_steps = steps
    finished_steps: Set[str] = set()
    working_steps: Dict[str, Step] = {}
    TIME_COMSUPTION = {chr(i): i - 4 for i in range(65, 91)}

    while len(finished_steps) != len(all_steps):

        WORKER_CAPACITY = 5

        tmp_finished = set()
        if len(working_steps):
            for (i, step) in working_steps.items():
                if step.finish_time <= current_time:
                    tmp_finished.add(step.name)
            finished_steps.update(tmp_finished)
            for finished_step in tmp_finished:
                del working_steps[finished_step]

        available_workers = WORKER_CAPACITY - len(working_steps)

        sorted_steps: List[Tuple[str, Step]] = sorted(
            unfinished_steps.items(), key=lambda x: x[0])
        dispatchable_works: List[str] = []
        for i, sorted_step in sorted_steps:
            if all([prev_step in finished_steps for prev_step in sorted_step.prev_steps]) or sorted_step.prev_steps == []:
                dispatchable_works.append(sorted_step.name)
                dispatchable_works.sort()

        for j in range(min(available_workers, len(dispatchable_works))):
            step = unfinished_steps[dispatchable_works[j]]
            step.finish_time = current_time + TIME_COMSUPTION[step.name]
            working_steps[dispatchable_works[j]] = step
            del unfinished_steps[dispatchable_works[j]]

        print(current_time, working_steps, finished_steps)
        current_time += 1

    return current_time - 1


# print(work(get_steps(TEST_CASE)))

with open('models/day07.txt') as f:
    instructions = [instruction for instruction in f.readlines()]
    print(work(get_steps(instructions)))
