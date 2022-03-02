from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.add_immediate_thumb import AddImmediateThumb


class AddImmediateThumbT1(AddImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 2, 0)
        rn = substring(instr, 5, 3)
        imm3 = substring(instr, 8, 6)
        setflags = not processor.in_it_block()
        return AddImmediateThumbT1(instr, setflags=setflags, d=rd, n=rn, imm32=imm3)
