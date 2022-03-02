from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrexh import Ldrexh


class LdrexhA1(Ldrexh):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rt == 15 or rn == 15:
            print('unpredictable')
        else:
            return LdrexhA1(instr, t=rt, n=rn)
