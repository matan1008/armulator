from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.str_register import StrRegister
from armulator.armv6.shift import decode_imm_shift


class StrRegisterA1(StrRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 6, 5)
        imm5 = substring(instr, 11, 7)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        index = bit_at(instr, 24)
        add = bit_at(instr, 23)
        w = bit_at(instr, 21)
        wback = (not index) or w
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        if rm == 15 or (wback and (rn == 15 or rn == rt)) or (arch_version() < 6 and wback and rm == rn):
            print('unpredictable')
        else:
            return StrRegisterA1(instr, add=add, wback=wback, index=index, m=rm, t=rt, n=rn, shift_t=shift_t,
                                 shift_n=shift_n)
