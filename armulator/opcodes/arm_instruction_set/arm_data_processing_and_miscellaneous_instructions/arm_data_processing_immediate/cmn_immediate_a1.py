from armulator.opcodes.abstract_opcodes.cmn_immediate import CmnImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import arm_expand_imm


class CmnImmediateA1(CmnImmediate, Opcode):
    def __init__(self, instruction, n, imm32):
        Opcode.__init__(self, instruction)
        CmnImmediate.__init__(self, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rn = instr[12:16]
        imm32 = arm_expand_imm(imm12)
        return CmnImmediateA1(instr, **{"n": rn.uint, "imm32": imm32})
