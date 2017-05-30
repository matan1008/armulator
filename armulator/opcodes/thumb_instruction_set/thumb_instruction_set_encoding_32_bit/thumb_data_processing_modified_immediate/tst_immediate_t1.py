from armulator.opcodes.abstract_opcodes.tst_immediate import TstImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import thumb_expand_imm_c


class TstImmediateT1(TstImmediate, Opcode):
    def __init__(self, instruction, n, imm32, carry):
        Opcode.__init__(self, instruction)
        TstImmediate.__init__(self, n, imm32, carry)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        imm3 = instr[17:20]
        rn = instr[12:16]
        i = instr[5:6]
        imm32, carry = thumb_expand_imm_c(i + imm3 + imm8, processor.registers.cpsr.get_c())
        if rn.uint in (13, 15):
            print "unpredictable"
        else:
            return TstImmediateT1(instr, **{"n": rn.uint, "imm32": imm32, "carry": carry})
