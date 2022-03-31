from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sxtab16 import Sxtab16


class Sxtab16T1(Sxtab16):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rotate = substring(instr, 5, 4)
        rd = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        rotation = rotate << 3
        if rd in (13, 15) or rn == 13 or rm in (13, 15):
            print('unpredictable')
        else:
            return Sxtab16T1(instr, m=rm, d=rd, n=rn, rotation=rotation)
