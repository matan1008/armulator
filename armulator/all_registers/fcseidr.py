from bitstring import BitArray


class FCSEIDR(object):
    """
    FCSE Process ID Register
    """

    def __init__(self):
        self.value = BitArray(length=32)

    def set_pid(self, pid):
        self.value[0:7] = pid

    def get_pid(self):
        return self.value[0:7]
