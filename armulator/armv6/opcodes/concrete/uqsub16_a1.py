from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.uqsub16 import Uqsub16


class Uqsub16A1(Uqsub16):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rd == 15 or rn == 15 or rm == 15:
            print('unpredictable')
        else:
            return Uqsub16A1(instr, m=rm, d=rd, n=rn)
