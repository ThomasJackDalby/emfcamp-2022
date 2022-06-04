import string
import random
from matplotlib.ft2font import ITALIC
from escpos.printer import Serial

def generate_uuid(length):
    chars = string.digits
    return "".join(random.choice(chars) for i in range(length-1))

p = Serial("COM4", baudrate=19200)

for i in range(2, 6):
    barcode = generate_uuid(12)
    p.barcode(barcode, "UPC-A")
    p.textln(f"{barcode} : {len(barcode)}")
    p.set(align="center")
    p.textln("-"*39)
p.cut()