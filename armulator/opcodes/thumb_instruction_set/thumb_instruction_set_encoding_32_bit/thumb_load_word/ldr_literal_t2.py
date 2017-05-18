from armulator.opcodes.abstract_opcodes.ldr_literal import LdrLiteral
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class LdrLiteralT2(LdrLiteral, Opcode):
    def __init__(self, instruction, add, imm32, t):
        Opcode.__init__(self, instruction)
        LdrLiteral.__init__(self, add, imm32, t)

    def is_pc_changing_opcode(self):
        return self.t == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rt = instr[16:20]
        add = instr[8]
        imm32 = zero_extend(imm12, 32)
        if rt.uint == 15 and processor.in_it_block() and not processor.last_in_it_block():
            print "unpredictable"
        else:
            return LdrLiteralT2(instr, **{"add": add, "imm32": imm32, "t": rt.uint})
