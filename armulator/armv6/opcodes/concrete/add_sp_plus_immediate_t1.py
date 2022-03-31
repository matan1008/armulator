from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.add_sp_plus_immediate import AddSpPlusImmediate


class AddSpPlusImmediateT1(AddSpPlusImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rd = substring(instr, 10, 8)
        setflags = False
        imm32 = imm8 << 2
        return AddSpPlusImmediateT1(instr, setflags=setflags, d=rd, imm32=imm32)
