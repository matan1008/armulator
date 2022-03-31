from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.clz import Clz


class ClzT1(Clz):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        rm1 = substring(instr, 19, 16)
        if rm in (13, 15) or rd in (13, 15) or rm != rm1:
            print('unpredictable')
        else:
            return ClzT1(instr, m=rm, d=rd)
