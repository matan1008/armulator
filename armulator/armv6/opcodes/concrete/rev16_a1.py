from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.rev16 import Rev16


class Rev16A1(Rev16):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        if rd == 15 or rm == 15:
            print('unpredictable')
        else:
            return Rev16A1(instr, m=rm, d=rd)
