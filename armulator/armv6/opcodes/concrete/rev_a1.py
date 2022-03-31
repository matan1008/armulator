from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.rev import Rev


class RevA1(Rev):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        if rd == 15 or rm == 15:
            print('unpredictable')
        else:
            return RevA1(instr, m=rm, d=rd)
