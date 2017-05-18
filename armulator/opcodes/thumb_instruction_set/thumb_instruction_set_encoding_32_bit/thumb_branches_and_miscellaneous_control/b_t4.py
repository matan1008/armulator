from armulator.opcodes.abstract_opcodes.b import B
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import sign_extend


class BT4(B, Opcode):
    def __init__(self, instruction, imm32):
        Opcode.__init__(self, instruction)
        B.__init__(self, imm32)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        imm11 = instr[21:32]
        j2 = instr[20:21]
        j1 = instr[18:19]
        imm10 = instr[6:16]
        s = instr[5:6]
        i1 = ~(j1 ^ s)
        i2 = ~(j2 ^ s)
        imm32 = sign_extend(s + i1 + i2 + imm10 + imm11 + "0b0", 32)
        if processor.in_it_block() and not processor.last_in_it_block():
            print "unpredictable"
        else:
            return BT4(instr, **{"imm32": imm32})
