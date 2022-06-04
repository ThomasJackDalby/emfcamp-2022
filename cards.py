import receipt_printer as p

NUMBERS = [
    " A "
    "222  2",
    "3"

]

def generate_card(suit, number):
    # list of strings?
    card = [" "*42 for i in range(20)]

    number = NUMBERS[number]


def print_card(card):
    for line in card:
        p.textln("".join(line))
    p.cut()

card = generate_card()
print_card(card)