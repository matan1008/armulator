from armulator.armv6.opcodes.abstract_opcodes.b import B
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import sign_extend


class BT3(B, Opcode):
    def __init__(self, instruction, imm32):
        Opcode.__init__(self, instruction)
        B.__init__(self, imm32)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        imm11 = instr[21:32]
        imm6 = instr[10:16]
        j2 = instr[20:21]
        j1 = instr[18:19]
        s = instr[5:6]
        imm32 = sign_extend(s + j2 + j1 + imm6 + imm11 + "0b0", 32)
        if processor.in_it_block():
            print "unpredictable"
        else:
            return BT3(instr, **{"imm32": imm32})
