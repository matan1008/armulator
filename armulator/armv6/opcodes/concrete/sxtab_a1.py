from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sxtab import Sxtab


class SxtabA1(Sxtab):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rotate = substring(instr, 11, 10)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        rotation = rotate * 8
        if rd == 15 or rm == 15:
            print('unpredictable')
        else:
            return SxtabA1(instr, m=rm, d=rd, n=rn, rotation=rotation)
