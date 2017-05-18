from armulator.opcodes.abstract_opcodes.add_sp_plus_immediate import AddSpPlusImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import thumb_expand_imm


class AddSpPlusImmediateT3(AddSpPlusImmediate, Opcode):
    def __init__(self, instruction, setflags, d, imm32):
        Opcode.__init__(self, instruction)
        AddSpPlusImmediate.__init__(self, setflags, d, imm32)

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
            return AddSpPlusImmediateT3(instr, **{"setflags": setflags, "d": rd.uint, "imm32": imm32})
