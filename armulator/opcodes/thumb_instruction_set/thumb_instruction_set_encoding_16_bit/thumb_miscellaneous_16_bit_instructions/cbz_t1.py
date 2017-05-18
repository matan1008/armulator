from armulator.opcodes.abstract_opcodes.cbz import Cbz
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class CbzT1(Cbz, Opcode):
    def __init__(self, instruction, nonzero, n, imm32):
        Opcode.__init__(self, instruction)
        Cbz.__init__(self, nonzero, n, imm32)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[13:16]
        imm5 = instr[8:13]
        i = instr[6:7]
        nonzero = instr[4]
        imm32 = zero_extend(i + imm5 + "0b0", 32)
        return CbzT1(instr, **{"nonzero": nonzero, "n": rn.uint, "imm32": imm32})
