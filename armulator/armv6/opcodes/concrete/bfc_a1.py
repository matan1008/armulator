from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.bfc import Bfc


class BfcA1(Bfc):
    @staticmethod
    def from_bitarray(instr, processor):
        lsb = substring(instr, 11, 7)
        rd = substring(instr, 15, 12)
        msb = substring(instr, 20, 16)
        if rd == 15:
            print('unpredictable')
        else:
            return BfcA1(instr, lsbit=lsb, msbit=msb, d=rd)
