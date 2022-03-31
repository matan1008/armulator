from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ssat16 import Ssat16


class Ssat16T1(Ssat16):
    @staticmethod
    def from_bitarray(instr, processor):
        sat_imm = substring(instr, 4, 0)
        rd = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        saturate_to = sat_imm + 1
        if rd in (13, 15) or rn in (13, 15):
            print('unpredictable')
        else:
            return Ssat16T1(instr, saturate_to=saturate_to, d=rd, n=rn)
