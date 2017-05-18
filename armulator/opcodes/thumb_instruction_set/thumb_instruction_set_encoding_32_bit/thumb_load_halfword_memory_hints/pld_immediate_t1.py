from armulator.opcodes.abstract_opcodes.pld_immediate import PldImmediate
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class PldImmediateT1(PldImmediate, Opcode):
    def __init__(self, instruction, add, is_pldw, n, imm32):
        Opcode.__init__(self, instruction)
        PldImmediate.__init__(self, add, is_pldw, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rn = instr[12:16]
        imm32 = zero_extend(imm12, 32)
        add = True
        is_pldw = instr[10]
        return PldImmediateT1(instr, **{"add": add, "is_pldw": is_pldw, "n": rn.uint, "imm32": imm32})
