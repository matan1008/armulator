from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sel import Sel


class SelA1(Sel):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rd == 15 or rm == 15 or rn == 15:
            print('unpredictable')
        else:
            return SelA1(instr, m=rm, d=rd, n=rn)
