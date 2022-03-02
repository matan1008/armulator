from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mrc_mrc2 import MrcMrc2


class MrcMrc2A2(MrcMrc2):
    @staticmethod
    def from_bitarray(instr, processor):
        coproc = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        if substring(coproc, 3, 1) == 0b101:
            raise UndefinedInstructionException()
        else:
            return MrcMrc2A2(instr, cp=coproc, t=rt)
