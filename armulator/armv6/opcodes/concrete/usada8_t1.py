from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.usada8 import Usada8


class Usada8T1(Usada8):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        ra = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rd in (13, 15) or rn in (13, 15) or rm in (13, 15) or ra == 13:
            print('unpredictable')
        else:
            return Usada8T1(instr, m=rm, a=ra, d=rd, n=rn)
