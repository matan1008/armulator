from armulator.opcodes.abstract_opcodes.mov_immediate import MovImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import arm_expand_imm_c


class MovImmediateA1(MovImmediate, Opcode):
    def __init__(self, instruction, setflags, d, imm32, carry):
        Opcode.__init__(self, instruction)
        MovImmediate.__init__(self, setflags, d, imm32, carry)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rd = instr[16:20]
        setflags = instr[11]
        imm32, carry = arm_expand_imm_c(imm12, processor.registers.cpsr.get_c())
        return MovImmediateA1(instr, **{"setflags": setflags, "d": rd.uint, "imm32": imm32, "carry": carry})
