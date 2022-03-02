from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sdiv import Sdiv


class SdivA1(Sdiv):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        rm = substring(instr, 11, 8)
        rd = substring(instr, 19, 16)
        if rd == 15 or rn == 15 or rm == 15:
            print('unpredictable')
        else:
            return SdivA1(instr, m=rm, d=rd, n=rn)
