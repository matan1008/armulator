from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.ssat import Ssat
from armulator.armv6.shift import decode_imm_shift


class SsatT1(Ssat):
    @staticmethod
    def from_bitarray(instr, processor):
        sat_imm = substring(instr, 4, 0)
        imm2 = substring(instr, 7, 6)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        rn = substring(instr, 19, 16)
        sh = bit_at(instr, 21)
        saturate_to = sat_imm + 1
        shift_t, shift_n = decode_imm_shift(sh << 2, chain(imm3, imm2, 2))
        if rd in (13, 15) or rn in (13, 15):
            print('unpredictable')
        else:
            return SsatT1(instr, saturate_to=saturate_to, d=rd, n=rn, shift_t=shift_t, shift_n=shift_n)
