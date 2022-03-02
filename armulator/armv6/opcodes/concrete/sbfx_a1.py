from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sbfx import Sbfx


class SbfxA1(Sbfx):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        lsb = substring(instr, 11, 7)
        rd = substring(instr, 15, 12)
        widthm1 = substring(instr, 20, 16)
        if rd == 15 or rn == 15:
            print('unpredictable')
        else:
            return SbfxA1(instr, lsbit=lsb, widthminus1=widthm1, d=rd, n=rn)
