from armulator.opcodes.abstract_opcodes.add_sp_plus_immediate import AddSpPlusImmediate
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class AddSpPlusImmediateT1(AddSpPlusImmediate, Opcode):
    def __init__(self, instruction, setflags, d, imm32):
        Opcode.__init__(self, instruction)
        AddSpPlusImmediate.__init__(self, setflags, d, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[8:16]
        rd = instr[5:8]
        setflags = False
        imm32 = zero_extend(imm8 + "0b00", 32)
        return AddSpPlusImmediateT1(instr, **{"setflags": setflags, "d": rd.uint, "imm32": imm32})
