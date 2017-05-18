from armulator.opcodes.abstract_opcodes.pld_literal import PldLiteral
from armulator.opcodes.opcode import Opcode


class PldLiteralA1(PldLiteral, Opcode):
    def __init__(self, instruction, add, imm32):
        Opcode.__init__(self, instruction)
        PldLiteral.__init__(self, add, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        add = instr[8]
        imm32 = "0b00000000000000000000" + imm12
        return PldLiteralA1(instr, **{"add": add, "imm32": imm32})
