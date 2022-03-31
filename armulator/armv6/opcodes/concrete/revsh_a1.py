from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.revsh import Revsh


class RevshA1(Revsh):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        if rm == 15 or rd == 15:
            print('unpredictable')
        else:
            return RevshA1(instr, m=rm, d=rd)
