from armulator.opcodes.abstract_opcodes.sub_sp_minus_immediate import SubSpMinusImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import thumb_expand_imm


class SubSpMinusImmediateT2(SubSpMinusImmediate, Opcode):
    def __init__(self, instruction, setflags, d, imm32):
        Opcode.__init__(self, instruction)
        SubSpMinusImmediate.__init__(self, setflags, d, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rd = instr[20:24]
        imm3 = instr[17:20]
        setflags = instr[11]
        i = instr[5:6]
        imm32 = thumb_expand_imm(i + imm3 + imm8)
        if rd.uint == 15 and not setflags:
            print "unpredictable"
        else:
            return SubSpMinusImmediateT2(instr, **{"setflags": setflags, "d": rd.uint, "imm32": imm32})
