from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.bx import Bx


class BxA1(Bx):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        return BxA1(instr, m=rm)
