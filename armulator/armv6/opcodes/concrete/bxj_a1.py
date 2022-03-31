from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.bxj import Bxj


class BxjA1(Bxj):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        if rm == 15:
            print('unpredictable')
        else:
            return BxjA1(instr, m=rm)
