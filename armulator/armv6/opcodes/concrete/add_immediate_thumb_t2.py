from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.add_immediate_thumb import AddImmediateThumb


class AddImmediateThumbT2(AddImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rdn = substring(instr, 10, 8)
        imm8 = substring(instr, 7, 0)
        set_flags = not processor.in_it_block()
        return AddImmediateThumbT2(instr, setflags=set_flags, d=rdn, n=rdn, imm32=imm8)
