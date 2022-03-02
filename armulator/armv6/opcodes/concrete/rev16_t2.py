from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.rev16 import Rev16


class Rev16T2(Rev16):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        rm1 = substring(instr, 19, 16)
        if rm in (13, 15) or rd in (13, 15) or rm != rm1:
            print('unpredictable')
        else:
            return Rev16T2(instr, m=rm, d=rd)
