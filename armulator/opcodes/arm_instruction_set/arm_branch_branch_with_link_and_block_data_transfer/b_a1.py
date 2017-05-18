from armulator.opcodes.abstract_opcodes.b import B
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import sign_extend


class BA1(B, Opcode):
    def __init__(self, instruction, imm32):
        Opcode.__init__(self, instruction)
        B.__init__(self, imm32)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = sign_extend(instr[8:32] + "0b00", 32)
        return BA1(instr, **{"imm32": imm32})
