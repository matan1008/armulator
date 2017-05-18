from armulator.opcodes.abstract_opcodes.mov_immediate import MovImmediate
from armulator.opcodes.opcode import Opcode


class MovImmediateA2(MovImmediate, Opcode):
    def __init__(self, instruction, d, imm32):
        Opcode.__init__(self, instruction)
        MovImmediate.__init__(self, False, d, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rd = instr[16:20]
        imm4 = instr[12:16]
        imm32 = "0b0000000000000000" + imm4 + imm12
        if rd.uint == 15:
            print "unpredictable"
        else:
            return MovImmediateA2(instr, **{"d": rd.uint, "imm32": imm32})
