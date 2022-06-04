import random
from escpos.printer import Serial

p = Serial("COM3", baudrate=19200)
EMPTY = "."
SHIP = "#"
HIT = "*"
MISS = "O"

COLUMNS = "ABCDEFGHIJ"
ROWS = "0123456789"

ships = [1, 2, 2, 3, 3, 3, 4, 4, 5]

# battle ships
class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.source = ["." for i in range(100)] 
        self.target = ["." for i in range(100)] 

# randomly place some ships
def place_ships(ships, grid):
    for ship in ships:
        while True:
            horizontal = bool(random.randint(0, 1))
            col = random.randint(0, len(COLUMNS)-1-(ship if horizontal else 0))
            row = random.randint(0, len(ROWS)-1-(ship if not horizontal else 0))
            x, y = (1, 0) if horizontal else (0, 1)
            indexes = [(row+y*i) * len(COLUMNS) + (col+x*i) for i in range(ship)]
            if all(grid[x] == EMPTY for x in indexes):
                print(f"ship {ship} {horizontal} {COLUMNS[col]}{row}")
                for index in indexes:
                    grid[index] = SHIP
                break

def print_grid(grid):
    p.set(double_width=True, align="center")
    p.textln("  "+COLUMNS+" ")
    p.textln(" +"+"-"*len(COLUMNS)+"+")
    for i in range(len(ROWS)):
        line = ROWS[i]+"|"+"".join(grid[i*len(COLUMNS):(i+1)*len(COLUMNS)])+"|"
        p.textln(line)
    p.textln(" +"+"-"*len(COLUMNS)+"+")

def print_player(player):
    p.set(double_height=True, double_width=True, bold=True)
    p.textln("BARCODE BATTLESHIPS")
    p.textln(player.name)
    p.textln()

    p.set(align="left", double_width=True)
    p.textln("Target")
    print_grid(player.target)

    p.set(align="left", double_width=True)
    p.textln("Harbour")
    print_grid(player.source)
    p.cut()

def get_index(col, row):
    return row * len(COLUMNS) + col

player_1 = Player("Andy")
player_2 = Player("Matt")

place_ships(ships, player_1.source)
place_ships(ships, player_2.source)

print_player(player_1)
print_player(player_2)

current = player_1
enemy = player_2

while True:
    current, enemy = enemy, current

    p.set(double_height=True, double_width=True, bold=True)
    p.textln(f"{current.name}'s turn!")
    p.cut()

    while True:
        try:
            col = COLUMNS.index(input())
            row = int(input())
            index = get_index(col, row)
            if index > 0 and index < len(enemy.source):
                break
        except:
            print("Incorrect coords")

    if enemy.source[index] == SHIP:
        current.target[index] = HIT
        enemy.source[index] = HIT
        print_player(current)
        print_player(enemy)
        current, enemy = enemy, current
    else:
        current.target[index] = MISS
        print_player(current)

