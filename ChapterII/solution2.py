"""
Solution to Task 2 from Chapter II for Skygate.

'What is the sum of all numbers in the document?'
Answer is 111754

Piotr Kopacki
piotrkopacki99@gmail.com
"""

import re


def get_numbers_from_string(string: str) -> list:
    """Returns all numbers (including negative) from a string"""
    return list(map(int, re.findall(r"(-?\d+)", string)))


if __name__ == "__main__":
    with open("skychallenge_accounting_input.txt") as f:
        data = f.read()

    answer = sum(get_numbers_from_string(data))

    print("What is the sum of all numbers in the document?")
    print("Answer: %s" % answer)
