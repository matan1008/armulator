from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mcr_mcr2 import McrMcr2


class McrMcr2A1(McrMcr2):
    @staticmethod
    def from_bitarray(instr, processor):
        coproc = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        if rt == 15:
            print('unpredictable')
        else:
            return McrMcr2A1(instr, cp=coproc, t=rt)
