from armulator.armv6.opcodes.abstract_opcodes.mvn_immediate import MvnImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import thumb_expand_imm_c


class MvnImmediateT1(MvnImmediate, Opcode):
    def __init__(self, instruction, setflags, d, imm32, carry):
        Opcode.__init__(self, instruction)
        MvnImmediate.__init__(self, setflags, d, imm32, carry)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rd = instr[20:24]
        imm3 = instr[17:20]
        setflags = instr[11]
        i = instr[5:6]
        imm32, carry = thumb_expand_imm_c(i + imm3 + imm8, processor.registers.cpsr.get_c())
        if rd.uint in (13, 15):
            print("unpredictable")
        else:
            return MvnImmediateT1(instr, **{"setflags": setflags, "d": rd.uint, "imm32": imm32, "carry": carry})
