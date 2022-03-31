from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.rsc_register import RscRegister
from armulator.armv6.shift import decode_imm_shift


class RscRegisterA1(RscRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 6, 5)
        imm5 = substring(instr, 11, 7)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        s = bit_at(instr, 20)
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        return RscRegisterA1(instr, setflags=s, m=rm, d=rd, n=rn, shift_t=shift_t, shift_n=shift_n)
