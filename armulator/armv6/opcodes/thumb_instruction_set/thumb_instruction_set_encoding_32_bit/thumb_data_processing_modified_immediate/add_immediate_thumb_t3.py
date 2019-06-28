from armulator.armv6.opcodes.abstract_opcodes.add_immediate_thumb import AddImmediateThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import thumb_expand_imm_c


class AddImmediateThumbT3(AddImmediateThumb, Opcode):
    def __init__(self, instruction, setflags, d, n, imm32):
        Opcode.__init__(self, instruction)
        AddImmediateThumb.__init__(self, setflags, d, n, imm32)

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
            print("unpredictable")
        else:
            return AddImmediateThumbT3(instr, **{"setflags": setflags, "d": rd.uint, "n": rn.uint, "imm32": imm32})
