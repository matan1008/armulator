from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.lsl_immediate import LslImmediate
from armulator.armv6.shift import decode_imm_shift


class LslImmediateT1(LslImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm5 = substring(instr, 10, 6)
        rd = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        set_flags = not processor.in_it_block()
        shift_n = decode_imm_shift(0b00, imm5)[1]
        return LslImmediateT1(instr, setflags=set_flags, m=rm, d=rd, shift_n=shift_n)
