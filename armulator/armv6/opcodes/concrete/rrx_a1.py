from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.rrx import Rrx


class RrxA1(Rrx):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        s = bit_at(instr, 20)
        return RrxA1(instr, setflags=s, m=rm, d=rd)
