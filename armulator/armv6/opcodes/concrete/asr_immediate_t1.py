from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.asr_immediate import AsrImmediate
from armulator.armv6.shift import decode_imm_shift


class AsrImmediateT1(AsrImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm5 = substring(instr, 10, 6)
        rd = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        set_flags = not processor.in_it_block()
        shift_n = decode_imm_shift(0b10, imm5)[1]
        return AsrImmediateT1(instr, setflags=set_flags, m=rm, d=rd, shift_n=shift_n)
