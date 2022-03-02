from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.strexb import Strexb


class StrexbT1(Strexb):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 3, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rd in (13, 15) or rt in (13, 15) or rn == 15 or rd == rn or rd == rt:
            print('unpredictable')
        else:
            return StrexbT1(instr, t=rt, d=rd, n=rn)
