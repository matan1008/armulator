from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.strexd import Strexd


class StrexdT1(Strexd):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 3, 0)
        rt2 = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rd in (13, 15) or rt in (13, 15) or rt2 in (13, 15) or rn == 15 or rd == rn or rd == rt or rd == rt2:
            print('unpredictable')
        else:
            return StrexdT1(instr, t=rt, t2=rt2, d=rd, n=rn)
