"""
Confident that your list of box IDs is complete, you're ready to find the boxes full of prototype fabric.

The boxes will have IDs which differ by exactly one character at the same position in both strings. For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
The IDs abcde and axcye are close, but they differ by two characters (the second and fourth). However, the IDs fghij and fguij differ by exactly one character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above, this is found by removing the differing character from either ID, producing fgij.)
"""
from typing import List
from collections import Counter

with open('models/day02.txt') as f:
    box_ids: List[str] = [line.strip() for line in f.readlines()]

def compare_two_strings(str1: str, str2: str) -> str:
    LENGTH = len(str1)
    
    same_letter_num = 0
    different_letter_pos = 0

    for i in range(LENGTH):
        if str1[i] == str2[i]:
            same_letter_num += 1
        else:
            different_letter_pos = i
 
    if same_letter_num == LENGTH -1:
        return str1[:different_letter_pos] + str1[different_letter_pos + 1:]
   

def find_the_box(box_ids: List[str]):
    LENGTH = len(box_ids[0])
    for i in range(len(box_ids)):
        for j in range(i+1, len(box_ids)):
            ret = compare_two_strings(box_ids[i], box_ids[j])
            if ret != None:
                return ret


print(find_the_box(box_ids))
