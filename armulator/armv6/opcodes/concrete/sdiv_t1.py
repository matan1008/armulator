from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sdiv import Sdiv


class SdivT1(Sdiv):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        if rm in (13, 15) or rn in (13, 15) or rd in (13, 15):
            print('unpredictable')
        else:
            return SdivT1(instr, m=rm, d=rd, n=rn)
