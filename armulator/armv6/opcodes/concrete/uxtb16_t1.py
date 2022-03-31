from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.uxtb16 import Uxtb16


class Uxtb16T1(Uxtb16):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rotate = substring(instr, 5, 4)
        rd = substring(instr, 11, 8)
        rotation = rotate << 3
        if rd in (13, 15) or rm in (13, 15):
            print('unpredictable')
        else:
            return Uxtb16T1(instr, m=rm, d=rd, rotation=rotation)
