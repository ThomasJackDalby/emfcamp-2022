import string
import random
import datetime
import json

from sqlalchemy import desc
import habville
from receipt_printer import Printer
p = Printer("COM3")

import requests
data = requests.get("https://www.emfcamp.org/schedule/2022.json").json()

# with open("data/schedule.json", "r", encoding="utf-8") as file:
#     data = json.load(file)

DAYS = ["", "", "Thursday", "Friday", "Saturday", "Sunday"]
def get_day(date):
    return DAYS[int(date.split(" ")[0][-1])]

def get_datetime(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

def get_time(date):
    return date.split(" ")[1][:5]

def print_talk(p, talk, barcode=False, description=False):
    p.set(align="left", bold=True, underline=True)
    p.textln(talk["title"])
    p.set(bold=False, underline=False)
    day = get_day(talk['start_date'])
    start = get_time(talk['start_date'])
    end = get_time(talk['end_date'])
    p.textln(f"{talk['speaker']}")
    p.textln(f"{day} | {start} - {end}")
    p.textln(f"{talk['venue']}")
    if description:
        p.textln(talk['description'])
    if barcode:
        barcode = "".join(random.choice(string.digits) for i in range(8)) + str(talk["id"]).zfill(3)
        p.barcode(barcode, "UPC-A")
    p.textln("-"*42)

def print_schedule(data, day):
    data = list(filter(lambda talk: get_day(talk["start_date"]) == day, data))
    p.set(double_height=True, double_width=True, bold=True, align="center")
    p.textln("EMF SCHEDULE")
    p.textln(day)
    cut = 0
    for talk in sorted(data, key=lambda talk: get_datetime(talk["start_date"])):
        print_talk(p, talk, True, False)
        cut += 1
        if cut >= 10:
            p.cut()
            cut = 0
    p.cut()

def print_custom(name):
    print("Please scan who you are?")
    if name is None:
        person = habville.scan_person()
        if person is None:
            print("Who even are you..?")
            return

    p.set(double_height=True, double_width=True, bold=True, align="center")
    p.textln("EMF SCHEDULE")
    p.textln(person.name.upper())
    
    while True:
        barcode = input("SCAN > ")
        talk_id = int(barcode[-4:-1])
        print(barcode, talk_id)
        if talk_id == 0:
            p.cut()
            return
        talk = next((talk for talk in data if talk["id"] == talk_id), None)
        if talk is not None:
            print_talk(p, talk)

def print_cancel():
    p.set(double_height=True, double_width=True, bold=True, align="center")
    p.textln("CANCEL CANCEL")
    p.barcode("00000000000", "UPC-A")
    p.textln("CANCEL CANCEL")
    p.cut()

if __name__ == "__main__":
    import sys
    

    if len(sys.argv) == 1:
        print_custom(None)
    else:
        name = sys.argv[1]
        print_custom(name)
    # print_schedule(data, "Saturday")
    # exit()