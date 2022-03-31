from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ror_immediate import RorImmediate
from armulator.armv6.shift import decode_imm_shift


class RorImmediateA1(RorImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        imm5 = substring(instr, 11, 7)
        rd = substring(instr, 15, 12)
        s = bit_at(instr, 20)
        shift_t, shift_n = decode_imm_shift(0b11, imm5)
        return RorImmediateA1(instr, setflags=s, m=rm, d=rd, shift_n=shift_n)
