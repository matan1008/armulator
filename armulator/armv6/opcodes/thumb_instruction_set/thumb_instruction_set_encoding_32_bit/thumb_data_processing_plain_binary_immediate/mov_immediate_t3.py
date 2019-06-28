from armulator.armv6.opcodes.abstract_opcodes.mov_immediate import MovImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class MovImmediateT3(MovImmediate, Opcode):
    def __init__(self, instruction, d, imm32):
        Opcode.__init__(self, instruction)
        MovImmediate.__init__(self, False, d, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rd = instr[20:24]
        imm3 = instr[17:20]
        imm4 = instr[12:16]
        i = instr[5:6]
        imm32 = zero_extend(imm4 + i + imm3 + imm8, 32)
        if rd.uint in (13, 15):
            print("unpredictable")
        else:
            return MovImmediateT3(instr, **{"d": rd.uint, "imm32": imm32})
