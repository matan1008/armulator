from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mcrr_mcrr2 import McrrMcrr2


class McrrMcrr2A2(McrrMcrr2):
    @staticmethod
    def from_bitarray(instr, processor):
        coproc = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        rt2 = substring(instr, 19, 16)
        if substring(coproc, 3, 1) == 0b101:
            raise UndefinedInstructionException()
        elif rt == 15 or rt2 == 15:
            print('unpredictable')
        else:
            return McrrMcrr2A2(instr, cp=coproc, t=rt, t2=rt2)
