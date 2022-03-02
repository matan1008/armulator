from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.usat import Usat
from armulator.armv6.shift import decode_imm_shift


class UsatT1(Usat):
    @staticmethod
    def from_bitarray(instr, processor):
        saturate_to = substring(instr, 4, 0)
        imm2 = substring(instr, 7, 6)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        rn = substring(instr, 19, 16)
        sh = bit_at(instr, 21)
        shift_t, shift_n = decode_imm_shift(sh << 2, chain(imm3, imm2, 2))
        if rd in (13, 15) or rn in (13, 15):
            print('unpredictable')
        else:
            return UsatT1(instr, saturate_to=saturate_to, d=rd, n=rn, shift_t=shift_t, shift_n=shift_n)
