from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mrs_application import MrsApplication


class MrsApplicationA1(MrsApplication):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 15, 12)
        if rd == 15:
            print('unpredictable')
        else:
            return MrsApplicationA1(instr, d=rd)
