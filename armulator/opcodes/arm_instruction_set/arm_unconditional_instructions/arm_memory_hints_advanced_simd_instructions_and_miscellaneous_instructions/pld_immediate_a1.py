from armulator.opcodes.abstract_opcodes.pld_immediate import PldImmediate
from armulator.opcodes.opcode import Opcode


class PldImmediateA1(PldImmediate, Opcode):
    def __init__(self, instruction, add, is_pldw, n, imm32):
        Opcode.__init__(self, instruction)
        PldImmediate.__init__(self, add, is_pldw, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rn = instr[12:16]
        is_pldw = instr[9]
        add = instr[8]
        imm32 = "0b00000000000000000000" + imm12
        return PldImmediateA1(instr, **{"add": add, "is_pldw": is_pldw, "n": rn.uint, "imm32": imm32})
