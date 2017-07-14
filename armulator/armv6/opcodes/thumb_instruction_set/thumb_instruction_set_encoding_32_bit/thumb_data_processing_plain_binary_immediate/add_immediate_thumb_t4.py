from armulator.armv6.opcodes.abstract_opcodes.add_immediate_thumb import AddImmediateThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class AddImmediateThumbT4(AddImmediateThumb, Opcode):
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
        i = instr[5:6]
        setflags = False
        imm32 = zero_extend(i + imm3 + imm8, 32)
        if rd.uint in (13, 15):
            print "unpredictable"
        else:
            return AddImmediateThumbT4(instr, **{"setflags": setflags, "d": rd.uint, "n": rn.uint, "imm32": imm32})
