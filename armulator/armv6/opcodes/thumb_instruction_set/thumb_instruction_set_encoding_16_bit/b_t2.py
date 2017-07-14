from armulator.armv6.opcodes.abstract_opcodes.b import B
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import sign_extend


class BT2(B, Opcode):
    def __init__(self, instruction, imm32):
        Opcode.__init__(self, instruction)
        B.__init__(self, imm32)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        imm11 = instr[5:16]
        imm32 = sign_extend(imm11 + "0b0", 32)
        if processor.in_it_block() and not processor.last_in_it_block():
            print "unpredictable"
        else:
            return BT2(instr, **{"imm32": imm32})
