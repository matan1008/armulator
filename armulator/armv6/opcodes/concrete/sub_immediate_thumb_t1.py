from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sub_immediate_thumb import SubImmediateThumb


class SubImmediateThumbT1(SubImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 2, 0)
        rn = substring(instr, 5, 3)
        imm3 = substring(instr, 8, 6)
        set_flags = not processor.in_it_block()
        return SubImmediateThumbT1(instr, setflags=set_flags, d=rd, n=rn, imm32=imm3)
