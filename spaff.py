    
    
from escpos.printer import Serial 
    
p = Serial("COM5", baudrate=19200)

while True:
    p.textln("-+"*21)