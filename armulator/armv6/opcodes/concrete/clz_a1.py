from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.clz import Clz


class ClzA1(Clz):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        if rm == 15 or rd == 15:
            print('unpredictable')
        else:
            return ClzA1(instr, m=rm, d=rd)
