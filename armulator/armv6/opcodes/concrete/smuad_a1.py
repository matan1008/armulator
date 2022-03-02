from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.smuad import Smuad


class SmuadA1(Smuad):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        m_swap = bit_at(instr, 5)
        rm = substring(instr, 11, 8)
        rd = substring(instr, 19, 16)
        if rd == 15 or rn == 15 or rm == 15:
            print('unpredictable')
        else:
            return SmuadA1(instr, m_swap=m_swap, m=rm, d=rd, n=rn)
