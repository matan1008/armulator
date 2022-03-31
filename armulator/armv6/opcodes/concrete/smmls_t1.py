from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.smmls import Smmls


class SmmlsT1(Smmls):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        ra = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        round_ = bit_at(instr, 4)
        if rd in (13, 15) or rn in (13, 15) or rm in (13, 15) or ra in (13, 15):
            print('unpredictable')
        else:
            return SmmlsT1(instr, round_=round_, m=rm, a=ra, d=rd, n=rn)
