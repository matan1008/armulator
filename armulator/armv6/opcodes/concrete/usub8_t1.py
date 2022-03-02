from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.usub8 import Usub8


class Usub8T1(Usub8):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        if rd in (13, 15) or rn in (13, 15) or rm in (13, 15):
            print('unpredictable')
        else:
            return Usub8T1(instr, m=rm, d=rd, n=rn)
