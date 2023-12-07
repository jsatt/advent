from collections import Counter


def read_file(test: bool = False):
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


CARD_VALUES = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13,
}


class Hand:
    def __init__(self, cards, bid, jokers_wild=False):
        self.cards = cards
        self.bid = int(bid)
        self.jokers_wild = jokers_wild
        self.type = self.get_hand_type()
        self.card_values = self.get_card_values()

    def __repr__(self):
        return f'<Hand: {self.cards} - {self.type}: {self.bid}'

    def __gt__(self, other):
        return (self.type, self.card_values) > (other.type, other.card_values)

    def get_card_values(self):
        values = CARD_VALUES.copy()
        if self.jokers_wild:
            values['J'] = 0
        return [values[c] for c in self.cards]

    def get_hand_type(self):
        cards = Counter(self.cards)
        if self.jokers_wild:
            jokers = cards.pop('J', 0)
            if not cards:
                cards.update({'A': jokers})
            else:
                cards.update({cards.most_common()[0][0]: jokers})
        card_counts = cards.most_common()
        if card_counts[0][1] == 5:
            # five of a kind
            value = 7
        elif card_counts[0][1] == 4:
            # four of a kind
            value = 6
        elif card_counts[0][1] == 3:
            if card_counts[1][1] == 2:
                # full house
                value = 5
            else:
                # three of a kind
                value = 4
        elif card_counts[0][1] == 2:
            if card_counts[1][1] == 2:
                # 2 pair
                value = 3
            else:
                # 1 pair
                value = 2
        else:
            # high card
            value = 1
        return value


def part_1(test=False):
    lines = read_file(test=test)
    hands = [Hand(*line.split()) for line in lines]
    hands.sort()
    return sum([h.bid * (r + 1) for r, h in enumerate(hands)])


def part_2(test=False):
    lines = read_file(test=test)
    hands = [Hand(*line.split(), jokers_wild=True) for line in lines]
    hands.sort()
    return sum([h.bid * (r + 1) for r, h in enumerate(hands)])


