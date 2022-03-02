from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.udiv import Udiv


class UdivT1(Udiv):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        if rm in (13, 15) or rn in (13, 15) or rd in (13, 15):
            print('unpredictable')
        else:
            return UdivT1(instr, m=rm, d=rd, n=rn)
