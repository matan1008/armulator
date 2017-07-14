from armulator.armv6.opcodes.abstract_opcodes.svc import Svc
from armulator.armv6.opcodes.opcode import Opcode


class SvcA1(Svc, Opcode):
    def __init__(self, instruction, imm32):
        Opcode.__init__(self, instruction)
        Svc.__init__(self, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = "0b00000000" + instr[8:32]
        return SvcA1(instr, **{"imm32": imm32})
