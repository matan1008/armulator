from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrexh import Ldrexh


class LdrexhT1(Ldrexh):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rt in (13, 15) or rn == 15:
            print('unpredictable')
        else:
            return LdrexhT1(instr, t=rt, n=rn)
