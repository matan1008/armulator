from armulator.armv6.bits_ops import substring
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.mul import Mul


class MulT1(Mul):
    @staticmethod
    def from_bitarray(instr, processor):
        rdm = substring(instr, 2, 0)
        rn = substring(instr, 5, 3)
        setflags = not processor.in_it_block()
        if arch_version() < 6 and rdm == rn:
            print('unpredictable')
        else:
            return MulT1(instr, setflags=setflags, m=rdm, d=rdm, n=rn)
