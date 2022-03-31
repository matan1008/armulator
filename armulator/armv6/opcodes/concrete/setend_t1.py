from armulator.armv6.bits_ops import bit_at
from armulator.armv6.opcodes.abstract_opcodes.setend import Setend


class SetendT1(Setend):
    @staticmethod
    def from_bitarray(instr, processor):
        set_bigend = bit_at(instr, 3)
        if processor.in_it_block():
            print('unpredictable')
        else:
            return SetendT1(instr, set_bigend=set_bigend)
