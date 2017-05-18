from armulator.opcodes.abstract_opcodes.sub_immediate_thumb import SubImmediateThumb
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class SubImmediateThumbT1(SubImmediateThumb, Opcode):
    def __init__(self, instruction, setflags, d, n, imm32):
        Opcode.__init__(self, instruction)
        SubImmediateThumb.__init__(self, setflags, d, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[13:16]
        rn = instr[10:13]
        imm3 = instr[7:10]
        imm32 = zero_extend(imm3, 32)
        set_flags = not processor.in_it_block()
        return SubImmediateThumbT1(instr, **{"setflags": set_flags, "d": rd.uint, "n": rn.uint, "imm32": imm32})
