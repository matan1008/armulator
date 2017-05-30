from armulator.opcodes.abstract_opcodes.sub_immediate_thumb import SubImmediateThumb
from armulator.opcodes.opcode import Opcode
from armulator.shift import thumb_expand_imm_c


class SubImmediateThumbT3(SubImmediateThumb, Opcode):
    def __init__(self, instruction, setflags, d, n, imm32):
        Opcode.__init__(self, instruction)
        SubImmediateThumb.__init__(self, setflags, d, n, imm32)

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
        if rd.uint == 13 or (rd.uint == 15 and not setflags) or rn.uint in (13, 15):
            print "unpredictable"
        else:
            return SubImmediateThumbT3(instr, **{"setflags": setflags, "d": rd.uint, "n": rn.uint, "imm32": imm32})
