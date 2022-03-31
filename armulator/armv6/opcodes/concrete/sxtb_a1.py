from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sxtb import Sxtb


class SxtbA1(Sxtb):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rotate = substring(instr, 11, 10)
        rd = substring(instr, 15, 12)
        rotation = rotate * 8
        if rd == 15 or rm == 15:
            print('unpredictable')
        else:
            return SxtbA1(instr, m=rm, d=rd, rotation=rotation)
