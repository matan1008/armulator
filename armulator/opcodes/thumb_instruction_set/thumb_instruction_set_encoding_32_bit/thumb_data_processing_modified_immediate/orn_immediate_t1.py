from armulator.opcodes.abstract_opcodes.orn_immediate import OrnImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import thumb_expand_imm_c


class OrnImmediateT1(OrnImmediate, Opcode):
    def __init__(self, instruction, setflags, d, n, imm32, carry):
        Opcode.__init__(self, instruction)
        OrnImmediate.__init__(self, setflags, d, n, imm32, carry)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rd = instr[20:24]
        imm3 = instr[17:20]
        rn = instr[12:16]
        setflags = instr[11]
        i = instr[5:6]
        imm32, carry = thumb_expand_imm_c(i + imm3 + imm8, processor.registers.cpsr.get_c())
        if rd.uint in (13, 15) or rn.uint == 13:
            print "unpredictable"
        else:
            return OrnImmediateT1(instr, **{"setflags": setflags, "d": rd.uint, "n": rn.uint, "imm32": imm32,
                                            "carry": carry})
