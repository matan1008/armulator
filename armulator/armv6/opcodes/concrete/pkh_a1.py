from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.pkh import Pkh
from armulator.armv6.shift import decode_imm_shift


class PkhA1(Pkh):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        tb_form = bit_at(instr, 6)
        imm5 = substring(instr, 11, 7)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        shift_t, shift_n = decode_imm_shift(tb_form << 1, imm5)
        if rd == 15 or rm == 15 or rn == 15:
            print('unpredictable')
        else:
            return PkhA1(instr, tb_form=tb_form, m=rm, d=rd, n=rn, shift_t=shift_t, shift_n=shift_n)
