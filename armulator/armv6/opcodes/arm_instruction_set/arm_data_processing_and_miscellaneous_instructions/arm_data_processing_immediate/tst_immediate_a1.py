from armulator.armv6.opcodes.abstract_opcodes.tst_immediate import TstImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import arm_expand_imm_c


class TstImmediateA1(TstImmediate, Opcode):
    def __init__(self, instruction, n, imm32, carry):
        Opcode.__init__(self, instruction)
        TstImmediate.__init__(self, n, imm32, carry)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rn = instr[12:16]
        imm32, carry = arm_expand_imm_c(imm12, processor.registers.cpsr.get_c())
        return TstImmediateA1(instr, **{"n": rn.uint, "imm32": imm32, "carry": carry})
