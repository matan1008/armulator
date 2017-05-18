from armulator.opcodes.abstract_opcodes.pld_immediate import PldImmediate
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class PldImmediateT2(PldImmediate, Opcode):
    def __init__(self, instruction, is_pldw, n, imm32):
        Opcode.__init__(self, instruction)
        PldImmediate.__init__(self, False, is_pldw, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rn = instr[12:16]
        is_pldw = instr[10]
        imm32 = zero_extend(imm8, 32)
        return PldImmediateT2(instr, **{"is_pldw": is_pldw, "n": rn.uint, "imm32": imm32})
