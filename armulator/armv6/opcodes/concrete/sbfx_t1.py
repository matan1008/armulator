from armulator.armv6.bits_ops import substring, chain
from armulator.armv6.opcodes.abstract_opcodes.sbfx import Sbfx


class SbfxT1(Sbfx):
    @staticmethod
    def from_bitarray(instr, processor):
        widthm1 = substring(instr, 4, 0)
        imm2 = substring(instr, 7, 6)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        rn = substring(instr, 19, 16)
        lsbit = chain(imm3, imm2, 2)
        if rd in (13, 15) or rn in (13, 15):
            print('unpredictable')
        else:
            return SbfxT1(instr, lsbit=lsbit, widthminus1=widthm1, d=rd, n=rn)
