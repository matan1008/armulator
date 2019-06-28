from armulator.armv6.opcodes.abstract_opcodes.ldrb_literal import LdrbLiteral
from armulator.armv6.opcodes.opcode import Opcode


class LdrbLiteralA1(LdrbLiteral, Opcode):
    def __init__(self, instruction, add, imm32, t):
        Opcode.__init__(self, instruction)
        LdrbLiteral.__init__(self, add, imm32, t)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        p = instr[7]
        add = instr[8]
        w = instr[10]
        imm12 = instr[20:32]
        rt = instr[16:20]
        imm32 = "0b00000000000000000000" + imm12
        if p == w or rt.uint == 15:
            print("unpredictable")
        else:
            return LdrbLiteralA1(instr, **{"add": add, "imm32": imm32, "t": rt.uint})
