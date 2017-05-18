from armulator.opcodes.abstract_opcodes.ldrsb_literal import LdrsbLiteral
from armulator.opcodes.opcode import Opcode


class LdrsbLiteralA1(LdrsbLiteral, Opcode):
    def __init__(self, instruction, add, imm32, t):
        Opcode.__init__(self, instruction)
        LdrsbLiteral.__init__(self, add, imm32, t)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        w = instr[10]
        p = instr[7]
        imm4_l = instr[-4:]
        imm4_h = instr[20:24]
        rt = instr[16:20]
        add = instr[8]
        imm32 = "0b000000000000000000000000" + imm4_h + imm4_l
        if p == w or rt.uint == 15:
            print "unpredictable"
        else:
            return LdrsbLiteralA1(instr, **{"add": add, "imm32": imm32, "t": rt.uint})
