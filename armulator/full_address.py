from bitstring import BitArray


class FullAddress(object):
    def __init__(self):
        self.physicaladdress = BitArray(length=40)
        self.ns = False
