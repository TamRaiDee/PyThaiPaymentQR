from .PromptPayField import PromptPayField
from PyCRC.CRCCCITT import CRCCCITT


class PromptPayQR:
    fields = {}

    def __init__(self):
        self.crc_obj = CRCCCITT("FFFF")
        self.addField("version", "01", "00")
        self.addField("onetime", "11", "01")
        self.addField("currency", "764", "53")
        self.addField("country", "TH", "58")

    def setAmount(self, amount):
        self.addField("amount", "%.2f" % round(amount, 2), "54")

    def addField(self, name, value, code):
        self.fields[code] = PromptPayField(code, name, value)

    def __str__(self):
        return self.toString()

    def toString(self):
        outStr = ""

        for _, field in sorted(self.fields.items()):
            outStr += str(field)

        crc = self.crc_obj.calculate(outStr + "6304")
        crchex = hex(crc)[2:].upper()
        crcField = PromptPayField("63", "crc16", crchex.zfill(4))
        outStr += str(crcField)

        return outStr
