from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sxth import Sxth


class SxthT1(Sxth):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        rotation = 0
        return SxthT1(instr, m=rm, d=rd, rotation=rotation)
