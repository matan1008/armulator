from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.bfi import Bfi


class BfiA1(Bfi):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        lsb = substring(instr, 11, 7)
        rd = substring(instr, 15, 12)
        msb = substring(instr, 20, 16)
        if rd == 15:
            print('unpredictable')
        else:
            return BfiA1(instr, lsbit=lsb, msbit=msb, d=rd, n=rn)
