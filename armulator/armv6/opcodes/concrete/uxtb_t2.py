from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.uxtb import Uxtb


class UxtbT2(Uxtb):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rotate = substring(instr, 5, 4)
        rd = substring(instr, 11, 8)
        rotation = rotate << 3
        if rd in (13, 15) or rm in (13, 15):
            print('unpredictable')
        else:
            return UxtbT2(instr, m=rm, d=rd, rotation=rotation)
