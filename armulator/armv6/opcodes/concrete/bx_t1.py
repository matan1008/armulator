from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.bx import Bx


class BxT1(Bx):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 6, 3)
        if processor.in_it_block() and not processor.last_in_it_block():
            print('unpredictable')
        else:
            return BxT1(instr, m=rm)
