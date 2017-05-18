from armulator.opcodes.abstract_opcodes.pld_literal import PldLiteral
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class PldLiteralT1(PldLiteral, Opcode):
    def __init__(self, instruction, add, imm32):
        Opcode.__init__(self, instruction)
        PldLiteral.__init__(self, add, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        add = instr[8]
        imm32 = zero_extend(imm12, 32)
        return PldLiteralT1(instr, **{"add": add, "imm32": imm32})
