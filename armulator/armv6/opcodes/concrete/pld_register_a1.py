from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.pld_register import PldRegister
from armulator.armv6.shift import decode_imm_shift


class PldRegisterA1(PldRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 6, 5)
        imm5 = substring(instr, 11, 7)
        rn = substring(instr, 19, 16)
        is_pldw = bit_at(instr, 22) == 0
        add = bit_at(instr, 23)
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        if rm == 15 or (rn == 15 and is_pldw):
            print('unpredictable')
        else:
            return PldRegisterA1(instr, add=add, is_pldw=is_pldw, m=rm, n=rn, shift_t=shift_t, shift_n=shift_n)
