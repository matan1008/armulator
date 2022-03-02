from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.usat16 import Usat16


class Usat16A1(Usat16):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        saturate_to = substring(instr, 19, 16)
        if rd == 15 or rn == 15:
            print('unpredictable')
        else:
            return Usat16A1(instr, saturate_to=saturate_to, d=rd, n=rn)
