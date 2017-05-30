from armulator.opcodes.abstract_opcodes.eor_immediate import EorImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import arm_expand_imm_c


class EorImmediateA1(EorImmediate, Opcode):
    def __init__(self, instruction, setflags, d, n, imm32, carry):
        Opcode.__init__(self, instruction)
        EorImmediate.__init__(self, setflags, d, n, imm32, carry)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rd = instr[16:20]
        rn = instr[12:16]
        setflags = instr[11]
        imm32, carry = arm_expand_imm_c(imm12, processor.core_registers.cpsr.get_c())
        return EorImmediateA1(instr, **{"setflags": setflags, "d": rd.uint, "n": rn.uint, "imm32": imm32,
                                        "carry": carry})
