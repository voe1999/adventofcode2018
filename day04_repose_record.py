"""
You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab. You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this is as close as you can safely get.

As you search the closet for anything that might help, you discover that you're not the first person to want to sneak in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the one whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....
The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour. (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)
"""

from typing import Set, List, Dict, NamedTuple, Tuple
from datetime import datetime
from collections import Counter
import re


class Nap(NamedTuple):
    guard_id: int
    sleep_minute: int
    wake_minute: int


class Record(NamedTuple):
    date: Tuple[int, int, int, int, int]
    content: str


with open('models/day04.txt') as f:
    records = [line.strip() for line in f.readlines()]

TEST_RECORDS = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""".split('\n')

def sort_records(records: List[str]) -> List[Record]:
    sorted_records = []
    regex = r'\[([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})\] (.*)'
    for record in records:
        match = re.match(regex, record)
        if match is not None:
            year, month, day, hour, minute, content = match.groups()
        sorted_records.append(
            Record((int(year), int(month), int(day), int(hour), int(minute)), content))
    sorted_records.sort()
    return sorted_records


# print(sort_records(records))


def get_naps_from_records(records: List[Record]) -> List[Nap]:
    current_guard_id = sleep_minute = wake_minute = None
    naps: List[Nap] = []
    for record in records:
        if 'Guard #' in record.content:
            id = re.search('Guard #([0-9]+).*', record.content).group(1)
            current_guard_id = int(id)
        if 'falls asleep' in record.content:
            sleep_minute = record.date[4]
        if 'wakes up' in record.content:
            wake_minute = record.date[4]
        if current_guard_id is not None and sleep_minute is not None and wake_minute is not None:
            naps.append(Nap(current_guard_id, sleep_minute, wake_minute))
            sleep_minute = wake_minute = None
    return naps



def get_sleepiest_guard(naps: List[Nap]) -> int:
    counts = Counter()
    for nap in naps:
        counts[nap.guard_id] += (nap.wake_minute - nap.sleep_minute)
    return counts.most_common(1)[0][0]

def get_most_common_minute(naps: List[Nap], guard_id: int) -> int:
    counts = Counter()
    for nap in naps:
        if guard_id == nap.guard_id:
            for minute in range(nap.sleep_minute, nap.wake_minute):
                counts[minute] += 1
    return counts.most_common(1)[0][0]

def main():
    naps = get_naps_from_records(sort_records(records))
    guard_id = get_sleepiest_guard(naps)
    minute = get_most_common_minute(naps, guard_id)
    print(guard_id * minute)
main()

"""
Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)
"""

def get_all_guards(naps: List[Nap]) -> Set[int]:
    counts = Counter()
    guards = set()
    for nap in naps:
        counts[nap.guard_id] += (nap.wake_minute - nap.sleep_minute)
    for count in counts.most_common():
        guards.add(count[0])
    return guards

def get_most_frequent_minute(naps: List[Nap], guard_id: int) -> Tuple[int, int]:
    counts = Counter()
    for nap in naps:
        if guard_id == nap.guard_id:
            for minute in range(nap.sleep_minute, nap.wake_minute):
                counts[minute] += 1
    return counts.most_common(1)[0]

def main2():
    naps = get_naps_from_records(sort_records(records))
    guards = get_all_guards(naps)
    minutes = {}
    for guard in guards:
        highest = get_most_frequent_minute(naps, guard)
        minutes[highest] = guard
    result = sorted(minutes.items(), key = lambda count: count[0][1], reverse = True)[0]
    minute = result[0][0]
    guard = result[1]
    print(minute * guard)

main2()
