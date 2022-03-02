from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.strexh import Strexh


class StrexhT1(Strexh):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 3, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rd in (13, 15) or rt in (13, 15) or rn == 15 or rd == rn or rd == rt:
            print('unpredictable')
        else:
            return StrexhT1(instr, t=rt, d=rd, n=rn)
