from armulator.armv6.opcodes.abstract_opcodes.ldrex import Ldrex
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zeros


class LdrexA1(Ldrex, Opcode):
    def __init__(self, instruction, imm32, t, n):
        Opcode.__init__(self, instruction)
        Ldrex.__init__(self, imm32, t, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[16:20]
        rn = instr[12:16]
        imm32 = zeros(32)
        if rn.uint == 15 or rt.uint == 15:
            print "unpredictable"
        else:
            return LdrexA1(instr, **{"imm32": imm32, "t": rt.uint, "n": rn.uint})
