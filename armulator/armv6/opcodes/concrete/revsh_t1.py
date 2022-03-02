from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.revsh import Revsh


class RevshT1(Revsh):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        return RevshT1(instr, m=rm, d=rd)
