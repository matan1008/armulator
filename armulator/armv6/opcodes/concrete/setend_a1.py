from armulator.armv6.bits_ops import bit_at
from armulator.armv6.opcodes.abstract_opcodes.setend import Setend


class SetendA1(Setend):
    @staticmethod
    def from_bitarray(instr, processor):
        set_bigend = bit_at(instr, 9)
        return SetendA1(instr, set_bigend=set_bigend)
