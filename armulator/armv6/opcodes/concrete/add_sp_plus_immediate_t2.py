from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.add_sp_plus_immediate import AddSpPlusImmediate


class AddSpPlusImmediateT2(AddSpPlusImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm7 = substring(instr, 6, 0)
        setflags = False
        d = 13
        imm32 = imm7 << 2
        return AddSpPlusImmediateT2(instr, setflags=setflags, d=d, imm32=imm32)
