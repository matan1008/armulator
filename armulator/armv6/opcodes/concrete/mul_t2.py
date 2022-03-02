from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mul import Mul


class MulT2(Mul):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        setflags = False
        if rd in (13, 15) or rn in (13, 15) or rm in (13, 15):
            print('unpredictable')
        else:
            return MulT2(instr, setflags=setflags, m=rm, d=rd, n=rn)
