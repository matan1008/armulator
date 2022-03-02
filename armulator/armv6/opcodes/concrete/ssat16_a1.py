from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ssat16 import Ssat16


class Ssat16A1(Ssat16):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        sat_imm = substring(instr, 19, 16)
        saturate_to = sat_imm + 1
        if rd == 15 or rn == 15:
            print('unpredictable')
        else:
            return Ssat16A1(instr, saturate_to=saturate_to, d=rd, n=rn)
