import random
import json

FILE_PATH = "data/people.json"

class Person:
    def __init__(self, name, code) -> None:
        self.name = name
        self.code = code

def get_person(barcode):
    barcode = barcode[:11] if len(barcode) > 11 else barcode # get rid of checksum
    person = next(person for person in data if person["barcode"] == barcode)
    if person is None:
        return person
    return Person(person["name"], person["barcode"])

def get_random_barcode():
    return "".join(str(random.randint(0, 9)) for i in range(11))

with open(FILE_PATH, "r") as file:
    data = json.load(file)

def register(name):
    barcode = get_random_barcode()
    data.append({
        "barcode" : barcode,
        "name" : name
    })
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

def print_people():
    from receipt_printer import Printer
    p = Printer("COM3")
    p.set(double_height=True, double_width=True, bold=True, align="center")
    p.textln()
    for person in data:
        p.set(double_height=True, double_width=True, bold=True, align="center")
        p.textln(person["name"])
        p.barcode(person["barcode"], "UPC-A")
        p.set()
        p.textln("-"*42)
    p.cut()

def scan_person():
    while True:
        barcode = input("SCAN > ")
        person = get_person(barcode)
        if person is not None:
            return person

if __name__ == "__main__":
    print_people()
    exit()
 
    import sys
    name = sys.argv[1]
    register(name)