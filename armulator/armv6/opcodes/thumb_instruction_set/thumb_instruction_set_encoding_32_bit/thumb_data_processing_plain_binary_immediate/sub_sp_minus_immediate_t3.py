from armulator.armv6.opcodes.abstract_opcodes.sub_sp_minus_immediate import SubSpMinusImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class SubSpMinusImmediateT3(SubSpMinusImmediate, Opcode):
    def __init__(self, instruction, setflags, d, imm32):
        Opcode.__init__(self, instruction)
        SubSpMinusImmediate.__init__(self, setflags, d, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rd = instr[20:24]
        imm3 = instr[17:20]
        i = instr[5:6]
        setflags = False
        imm32 = zero_extend(i + imm3 + imm8, 32)
        if rd.uint == 15:
            print "unpredictable"
        else:
            return SubSpMinusImmediateT3(instr, **{"setflags": setflags, "d": rd.uint, "imm32": imm32})
