from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.uxth import Uxth


class UxthT1(Uxth):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        rotation = 0
        return UxthT1(instr, m=rm, d=rd, rotation=rotation)
