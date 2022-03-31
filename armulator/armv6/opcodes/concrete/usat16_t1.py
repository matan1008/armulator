from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.usat16 import Usat16


class Usat16T1(Usat16):
    @staticmethod
    def from_bitarray(instr, processor):
        saturate_to = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        if rd in (13, 15) or rn in (13, 15):
            print('unpredictable')
        else:
            return Usat16T1(instr, saturate_to=saturate_to, d=rd, n=rn)
