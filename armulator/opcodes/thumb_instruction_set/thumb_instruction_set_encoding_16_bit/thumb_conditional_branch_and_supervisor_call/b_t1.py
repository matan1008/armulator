from armulator.opcodes.abstract_opcodes.b import B
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import sign_extend


class BT1(B, Opcode):
    def __init__(self, instruction, imm32):
        Opcode.__init__(self, instruction)
        B.__init__(self, imm32)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[8:16]
        imm32 = sign_extend(imm8 + "0b0", 32)
        if processor.in_it_block():
            print "unpredictable"
        else:
            return BT1(instr, **{"imm32": imm32})
