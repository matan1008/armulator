from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.mov_immediate import MovImmediate
from armulator.armv6.shift import arm_expand_imm_c


class MovImmediateA1(MovImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = substring(instr, 11, 0)
        rd = substring(instr, 15, 12)
        setflags = bit_at(instr, 20)
        imm32, carry = arm_expand_imm_c(imm12, processor.registers.cpsr.c)
        return MovImmediateA1(instr, setflags=setflags, d=rd, imm32=imm32, carry=carry)
