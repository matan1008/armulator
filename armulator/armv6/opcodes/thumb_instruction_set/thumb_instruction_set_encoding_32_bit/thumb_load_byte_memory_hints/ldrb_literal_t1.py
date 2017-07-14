from armulator.armv6.opcodes.abstract_opcodes.ldrb_literal import LdrbLiteral
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class LdrbLiteralT1(LdrbLiteral, Opcode):
    def __init__(self, instruction, add, imm32, t):
        Opcode.__init__(self, instruction)
        LdrbLiteral.__init__(self, add, imm32, t)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rt = instr[16:20]
        add = instr[8]
        imm32 = zero_extend(imm12, 32)
        if rt.uint == 13:
            print "unpredictable"
        else:
            return LdrbLiteralT1(instr, **{"add": add, "imm32": imm32, "t": rt.uint})
