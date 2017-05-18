from armulator.opcodes.abstract_opcodes.sbc_immediate import SbcImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import arm_expand_imm


class SbcImmediateA1(SbcImmediate, Opcode):
    def __init__(self, instruction, setflags, d, n, imm32):
        Opcode.__init__(self, instruction)
        SbcImmediate.__init__(self, setflags, d, n, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rd = instr[16:20]
        rn = instr[12:16]
        setflags = instr[11]
        imm32 = arm_expand_imm(imm12)
        return SbcImmediateA1(instr, **{"setflags": setflags, "d": rd.uint, "n": rn.uint, "imm32": imm32})
