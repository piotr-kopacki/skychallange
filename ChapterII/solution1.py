"""
Solution to Task 1 from Chapter II for Skygate.

'How many skyphrases are valid?'
Answer is 383

Piotr Kopacki
piotrkopacki99@gmail.com
"""


def count_valid_skyphrases(data):
    """Returns the count of valid skyphrases"""
    count = 0
    for phrase in data:
        phrase_split = phrase.split()
        if len(phrase_split) == len(set(phrase_split)):
            count += 1
    return count


if __name__ == "__main__":
    with open("skychallenge_skyphrase_input.txt") as f:
        data = f.readlines()

    answer = count_valid_skyphrases(data)

    print("How many skyphrases are valid?")
    print("Answer: %s" % answer)
