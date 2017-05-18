from armulator.opcodes.abstract_opcodes.ldrsh_literal import LdrshLiteral
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class LdrshLiteralT1(LdrshLiteral, Opcode):
    def __init__(self, instruction, add, imm32, t):
        Opcode.__init__(self, instruction)
        LdrshLiteral.__init__(self, add, imm32, t)

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
            return LdrshLiteralT1(instr, **{"add": add, "imm32": imm32, "t": rt.uint})
