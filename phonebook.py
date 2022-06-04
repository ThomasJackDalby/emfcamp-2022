# scrape the phonebook website for EMF and print out a receipt with the numbers on

import requests
from bs4 import BeautifulSoup

URL = "https://guru3.eventphone.de/event.exe/phonebook?order=extension&page="

contacts = []
for i in range(36):
    response = requests.get(URL+str(i))
    soup = BeautifulSoup(response.content, 'html.parser')
    phonebook = soup.find(id="phonebook")
    if phonebook is None:
        continue
    
    for entry in phonebook.find_all("tr"):
        bits = entry.find_all("td")
        if len(bits) == 0:
            continue

        extension = bits[0].find("a")["href"].split(":")[1]
        name = bits[1].text.strip()
        location = bits[3].text.strip()
        contacts.append((extension, name, location))

import receipt_printer as p

p.set_title()
p.textln("EMF Phonebook")
p.set()
for contact in contacts:
    p.textln("-"*42)
    p.textln(contact[0])
    p.textln(contact[1])
    p.textln(contact[2])
p.cut()