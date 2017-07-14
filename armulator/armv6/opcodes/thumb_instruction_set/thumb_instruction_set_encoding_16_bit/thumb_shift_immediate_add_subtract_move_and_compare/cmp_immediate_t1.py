from armulator.armv6.opcodes.abstract_opcodes.cmp_immediate import CmpImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class CmpImmediateT1(CmpImmediate, Opcode):
    def __init__(self, instruction, n, imm32):
        Opcode.__init__(self, instruction)
        CmpImmediate.__init__(self, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[5:8]
        imm8 = instr[8:16]
        imm32 = zero_extend(imm8, 32)
        return CmpImmediateT1(instr, **{"n": rn.uint, "imm32": imm32})
