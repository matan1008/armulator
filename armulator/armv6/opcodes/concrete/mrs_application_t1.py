from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mrs_application import MrsApplication


class MrsApplicationT1(MrsApplication):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 11, 8)
        if rd in (13, 15):
            print('unpredictable')
        else:
            return MrsApplicationT1(instr, d=rd)
