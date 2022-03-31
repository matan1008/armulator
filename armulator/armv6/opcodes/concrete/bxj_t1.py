from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.bxj import Bxj


class BxjT1(Bxj):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 19, 16)
        if rm in (13, 15) or (processor.in_it_block() and not processor.last_in_it_block()):
            print('unpredictable')
        else:
            return BxjT1(instr, m=rm)
