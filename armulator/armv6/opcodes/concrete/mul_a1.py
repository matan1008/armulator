from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.mul import Mul


class MulA1(Mul):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        rm = substring(instr, 11, 8)
        rd = substring(instr, 19, 16)
        setflags = bit_at(instr, 20)
        if rd == 15 or rm == 15 or rn == 15 or (rn == rd and arch_version() < 6):
            print('unpredictable')
        else:
            return MulA1(instr, setflags=setflags, m=rm, d=rd, n=rn)
