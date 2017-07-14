from armulator.armv6.opcodes.abstract_opcodes.ldr_literal import LdrLiteral
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class LdrLiteralT1(LdrLiteral, Opcode):
    def __init__(self, instruction, add, imm32, t):
        Opcode.__init__(self, instruction)
        LdrLiteral.__init__(self, add, imm32, t)

    def is_pc_changing_opcode(self):
        return self.t == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[8:16]
        rt = instr[5:8]
        add = True
        imm32 = zero_extend(imm8 + "0b00", 32)
        return LdrLiteralT1(instr, **{"add": add, "imm32": imm32, "t": rt.uint})
