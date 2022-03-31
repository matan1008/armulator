from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.uxtb16 import Uxtb16


class Uxtb16A1(Uxtb16):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rotate = substring(instr, 11, 10)
        rd = substring(instr, 15, 12)
        rotation = rotate * 8
        if rd == 15 or rm == 15:
            print('unpredictable')
        else:
            return Uxtb16A1(instr, m=rm, d=rd, rotation=rotation)
