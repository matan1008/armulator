from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mov_immediate import MovImmediate


class MovImmediateT1(MovImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 10, 8)
        imm8 = substring(instr, 7, 0)
        set_flags = not processor.in_it_block()
        carry = processor.registers.cpsr.c
        return MovImmediateT1(instr, setflags=set_flags, d=rd, imm32=imm8, carry=carry)
