from armulator.armv6.bits_ops import substring, chain
from armulator.armv6.opcodes.abstract_opcodes.bfc import Bfc


class BfcT1(Bfc):
    @staticmethod
    def from_bitarray(instr, processor):
        msb = substring(instr, 4, 0)
        imm2 = substring(instr, 7, 6)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        lsbit = chain(imm3, imm2, 2)
        if rd in (13, 15):
            print('unpredictable')
        else:
            return BfcT1(instr, lsbit=lsbit, msbit=msb, d=rd)
