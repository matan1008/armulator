from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.cmn_register import CmnRegister
from armulator.armv6.shift import decode_imm_shift


class CmnRegisterA1(CmnRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 6, 5)
        imm5 = substring(instr, 11, 7)
        rn = substring(instr, 19, 16)
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        return CmnRegisterA1(instr, m=rm, n=rn, shift_t=shift_t, shift_n=shift_n)
