from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.eor_register import EorRegister
from armulator.armv6.shift import decode_imm_shift


class EorRegisterA1(EorRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 6, 5)
        imm5 = substring(instr, 11, 7)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        s = bit_at(instr, 20)
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        return EorRegisterA1(instr, setflags=s, m=rm, d=rd, n=rn, shift_t=shift_t, shift_n=shift_n)
