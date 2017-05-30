from armulator.opcodes.abstract_opcodes.sub_sp_minus_immediate import SubSpMinusImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import arm_expand_imm_c


class SubSpMinusImmediateA1(SubSpMinusImmediate, Opcode):
    def __init__(self, instruction, setflags, d, imm32):
        Opcode.__init__(self, instruction)
        SubSpMinusImmediate.__init__(self, setflags, d, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rd = instr[16:20]
        rn = instr[12:16]
        setflags = instr[11]
        imm32, carry = arm_expand_imm_c(imm12, processor.registers.cpsr.get_c())
        return SubSpMinusImmediateA1(instr, **{"setflags": setflags, "d": rd.uint, "imm32": imm32})
