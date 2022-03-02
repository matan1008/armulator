from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrexb import Ldrexb


class LdrexbA1(Ldrexb):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rt == 15 or rn == 15:
            print('unpredictable')
        else:
            return LdrexbA1(instr, t=rt, n=rn)
