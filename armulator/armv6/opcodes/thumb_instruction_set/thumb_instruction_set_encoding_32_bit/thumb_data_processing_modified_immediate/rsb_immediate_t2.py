from armulator.armv6.opcodes.abstract_opcodes.rsb_immediate import RsbImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import thumb_expand_imm


class RsbImmediateT2(RsbImmediate, Opcode):
    def __init__(self, instruction, setflags, d, n, imm32):
        Opcode.__init__(self, instruction)
        RsbImmediate.__init__(self, setflags, d, n, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rd = instr[20:24]
        imm3 = instr[17:20]
        rn = instr[12:16]
        setflags = instr[11]
        i = instr[5:6]
        imm32 = thumb_expand_imm(i + imm3 + imm8)
        if rd.uint in (13, 15) or rn.uint in (13, 15):
            print("unpredictable")
        else:
            return RsbImmediateT2(instr, **{"setflags": setflags, "d": rd.uint, "n": rn.uint, "imm32": imm32})
