from armulator.armv6.opcodes.abstract_opcodes.svc import Svc
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import sign_extend


class SvcT1(Svc, Opcode):
    def __init__(self, instruction, imm32):
        Opcode.__init__(self, instruction)
        Svc.__init__(self, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[8:16]
        imm32 = sign_extend(imm8, 32)
        return SvcT1(instr, **{"imm32": imm32})
