from armulator.armv6.opcodes.abstract_opcodes.ldr_literal import LdrLiteral
from armulator.armv6.opcodes.opcode import Opcode


class LdrLiteralA1(LdrLiteral, Opcode):
    def __init__(self, instruction, add, imm32, t):
        Opcode.__init__(self, instruction)
        LdrLiteral.__init__(self, add, imm32, t)

    def is_pc_changing_opcode(self):
        return self.t == 15

    @staticmethod
    def from_bitarray(instr, processor):
        index = instr[7]
        add = instr[8]
        w = instr[10]
        imm12 = instr[20:32]
        rt = instr[16:20]
        if index == w:
            print("unpredictable")
        else:
            imm32 = "0b00000000000000000000" + imm12
            return LdrLiteralA1(instr, **{"add": add, "imm32": imm32, "t": rt.uint})
