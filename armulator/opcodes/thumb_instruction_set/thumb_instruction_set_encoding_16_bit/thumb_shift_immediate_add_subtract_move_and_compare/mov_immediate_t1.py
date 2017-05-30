from armulator.opcodes.abstract_opcodes.mov_immediate import MovImmediate
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class MovImmediateT1(MovImmediate, Opcode):
    def __init__(self, instruction, setflags, d, imm32, carry):
        Opcode.__init__(self, instruction)
        MovImmediate.__init__(self, setflags, d, imm32, carry)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[5:8]
        imm8 = instr[8:16]
        imm32 = zero_extend(imm8, 32)
        set_flags = not processor.in_it_block()
        carry = processor.core_registers.cpsr.get_c()
        return MovImmediateT1(instr, **{"setflags": set_flags, "d": rd.uint, "imm32": imm32, "carry": carry})
