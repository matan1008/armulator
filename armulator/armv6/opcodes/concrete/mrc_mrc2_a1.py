from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mrc_mrc2 import MrcMrc2


class MrcMrc2A1(MrcMrc2):
    @staticmethod
    def from_bitarray(instr, processor):
        coproc = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        return MrcMrc2A1(instr, cp=coproc, t=rt)
