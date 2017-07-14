from armulator.armv6.opcodes.abstract_opcodes.sub_sp_minus_immediate import SubSpMinusImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class SubSpMinusImmediateT1(SubSpMinusImmediate, Opcode):
    def __init__(self, instruction, setflags, d, imm32):
        Opcode.__init__(self, instruction)
        SubSpMinusImmediate.__init__(self, setflags, d, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm7 = instr[9:16]
        setflags = False
        d = 13
        imm32 = zero_extend(imm7 + "0b00", 32)
        return SubSpMinusImmediateT1(instr, **{"setflags": setflags, "d": d, "imm32": imm32})
