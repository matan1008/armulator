from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrexd import Ldrexd


class LdrexdT1(Ldrexd):
    @staticmethod
    def from_bitarray(instr, processor):
        rt2 = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rt in (13, 15) or rt2 in (13, 15) or rn == 15 or rt2 == rt:
            print('unpredictable')
        else:
            return LdrexdT1(instr, t=rt, t2=rt2, n=rn)
