import string
import random
import datetime
import json
from escpos.printer import Serial
from regex import D 

p = Serial("COM4", baudrate=19200)

class Item:
    def __init__(self, barcode, name):
        self.name = name
        self.barcode = barcode

items = [
    Item("74837465937","Bread"),
    Item("11773366448", "Egg"),
    Item("23523565435", "Bacon")
]

def print_menu():
    p.set(double_height=True, double_width=True, bold=True, align="center")
    p.textln("BREAKFAST MENU")
    p.textln()
    for item in items:
        p.set(bold=True)
        p.textln(item.name)
        p.set(bold=False)
        # p.textln(item.description)
        p.barcode(item.barcode, "UPC-A")
        p.textln("-"*42)
    p.textln("Complete")
    p.barcode("00000000000", "UPC-A")
    p.cut()

def create_order():
    order_id = random.randint(0, 100)
    order = {}
    while True:
        barcode = input("SCAN > ")[:-1]
        if int(barcode) == 0:
            p.set(double_height=True, double_width=True, bold=True, align="center", underline=True)
            p.textln(f"ORDER #{order_id}")
            p.textln()
            p.set(double_height=True, double_width=True, align="left")
            for item in order:
                p.textln(f"{item.name} x {order[item]}")
            p.cut()
            p.set(double_height=True, double_width=True, bold=True, align="center", underline=True)
            p.textln(f"ORDER #{order_id}")
            p.textln()
            p.set(double_height=True, double_width=True, align="left")
            p.textln("Please retain for collection.")
            p.cut()
            return
        item = next((item for item in items if item.barcode == barcode), None)
        if item is not None:
            if not item in order:
                order[item] = 0
            order[item] += 1
            print(f"Added 1 {item.name}")
        

create_order()