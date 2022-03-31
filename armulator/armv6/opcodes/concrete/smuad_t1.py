from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.smuad import Smuad


class SmuadT1(Smuad):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        m_swap = bit_at(instr, 4)
        if rd in (13, 15) or rn in (13, 15) or rm in (13, 15):
            print('unpredictable')
        else:
            return SmuadT1(instr, m_swap=m_swap, m=rm, d=rd, n=rn)
