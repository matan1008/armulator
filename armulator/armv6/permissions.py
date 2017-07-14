from bitstring import BitArray


class Permissions(object):
    def __init__(self):
        self.ap = BitArray(length=3)
        self.xn = False
        self.pxn = False
