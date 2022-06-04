from dataclasses import dataclass

@dataclass
class Style:
    double_height = False
    double_width = False
    bold = False

class TestPrinter:

    def __init__(self):
        self.width = 42
        self.margin = 2

        print()
        self._print_start()

    def textln(self, text):
        while len(text) > self.width:
            self._print(text[:self.width])
            text = text[self.width:]
        self._print(text)

    def barcode(self, code, type):
        self._print_blank()
        if len(code) % 2 != 0:
            code += "0"
        margin = " "*(self.margin+(self.width - len(code))//2)
        print("|"+margin+"|"*(len(code))+margin+"|")
        print("|"+margin+code+margin+"|")
        self._print_blank()

    def cut(self):
        self._print_end()
        print()
        self._print_start()

    def _print_blank(self):
        print("|"+" "*(self.width+self.margin*2)+"|")

    def _print_edge(self):
        print("+"+"-"*(self.width+self.margin*2)+"+")

    def _print_start(self):
        self._print_edge()
        self._print_blank()

    def _print_end(self):
        self._print_edge()

    def _print(self, text):
        print("|"+" "*self.margin+str.ljust(text, self.width)+" "*self.margin+"|")

class Printer:

    def __init__(self, com_port):
        from escpos.printer import Serial
        self.p = Serial("COM3", baudrate=19200)

    def textln(self, text=""):
        self.p.textln(text)

    def set_title():
        set(double_height=True, double_width=True, bold=True, align="center")

    def set(self, double_height=False, double_width=False, bold=False, align="left", underline=False):
        self.p.set(double_height=double_height, double_width=double_width, bold=bold, align=align, underline=underline)

    def barcode(self, barcode, type):
        self.p.barcode(barcode, type)

    def cut(self):
        self.p.cut()

if __name__ == "__main__":
    p = TestPrinter()
    p.textln("blah blah blah blah blah blah blah blah blah blah blah blah")
    p.barcode("01234567890", "UPC-A")
    p.cut()