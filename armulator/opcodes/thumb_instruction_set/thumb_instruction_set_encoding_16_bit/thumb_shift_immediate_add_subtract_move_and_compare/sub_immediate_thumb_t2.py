from armulator.opcodes.abstract_opcodes.sub_immediate_thumb import SubImmediateThumb
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class SubImmediateThumbT2(SubImmediateThumb, Opcode):
    def __init__(self, instruction, setflags, d, n, imm32):
        Opcode.__init__(self, instruction)
        SubImmediateThumb.__init__(self, setflags, d, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rdn = instr[5:8]
        imm8 = instr[8:16]
        imm32 = zero_extend(imm8, 32)
        set_flags = not processor.in_it_block()
        return SubImmediateThumbT2(instr, **{"setflags": set_flags, "d": rdn.uint, "n": rdn.uint, "imm32": imm32})
