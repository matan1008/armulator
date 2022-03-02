from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.qadd16 import Qadd16


class Qadd16A1(Qadd16):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rd == 15 or rn == 15 or rm == 15:
            print('unpredictable')
        else:
            return Qadd16A1(instr, m=rm, d=rd, n=rn)
