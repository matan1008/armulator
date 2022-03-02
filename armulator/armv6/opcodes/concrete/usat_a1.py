from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.usat import Usat
from armulator.armv6.shift import decode_imm_shift


class UsatA1(Usat):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        sh = bit_at(instr, 6)
        imm5 = substring(instr, 11, 7)
        rd = substring(instr, 15, 12)
        saturate_to = substring(instr, 20, 16)
        shift_t, shift_n = decode_imm_shift(sh << 1, imm5)
        if rd == 15 or rn == 15:
            print('unpredictable')
        else:
            return UsatA1(instr, saturate_to=saturate_to, d=rd, n=rn, shift_t=shift_t, shift_n=shift_n)
