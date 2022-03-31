from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.strbt import Strbt
from armulator.armv6.shift import decode_imm_shift


class StrbtA2(Strbt):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 6, 5)
        imm5 = substring(instr, 11, 7)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        add = bit_at(instr, 23)
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        post_index = True
        if rt == 15 or rn == 15 or rn == rt or rm or (arch_version() < 6 and rm == rn):
            print('unpredictable')
        else:
            return StrbtA2(instr, register_form=True, add=add, post_index=post_index, t=rt, n=rn, m=rm, shift_t=shift_t,
                           shift_n=shift_n)
