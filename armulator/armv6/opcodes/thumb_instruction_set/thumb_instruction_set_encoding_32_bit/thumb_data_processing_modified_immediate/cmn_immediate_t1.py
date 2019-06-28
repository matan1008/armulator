from armulator.armv6.opcodes.abstract_opcodes.cmn_immediate import CmnImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import thumb_expand_imm


class CmnImmediateT1(CmnImmediate, Opcode):
    def __init__(self, instruction, n, imm32):
        Opcode.__init__(self, instruction)
        CmnImmediate.__init__(self, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        imm3 = instr[17:20]
        rn = instr[12:16]
        i = instr[5:6]
        imm32 = thumb_expand_imm(i + imm3 + imm8)
        if rn.uint == 15:
            print("unpredictable")
        else:
            return CmnImmediateT1(instr, **{"n": rn.uint, "imm32": imm32})
