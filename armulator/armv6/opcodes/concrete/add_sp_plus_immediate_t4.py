from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.add_sp_plus_immediate import AddSpPlusImmediate


class AddSpPlusImmediateT4(AddSpPlusImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        i = bit_at(instr, 26)
        setflags = False
        imm32 = chain(i, chain(imm3, imm8, 8), 11)
        if rd == 15:
            print('unpredictable')
        else:
            return AddSpPlusImmediateT4(instr, setflags=setflags, d=rd, imm32=imm32)
