from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mcrr_mcrr2 import McrrMcrr2


class McrrMcrr2T1(McrrMcrr2):
    @staticmethod
    def from_bitarray(instr, processor):
        coproc = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        rt2 = substring(instr, 19, 16)
        if rt == 15 or rt2 == 15 or (rt == 13 or rt2 == 13):
            print('unpredictable')
        else:
            return McrrMcrr2T1(instr, cp=coproc, t=rt, t2=rt2)
