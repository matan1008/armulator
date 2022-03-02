from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.add_immediate_thumb import AddImmediateThumb


class AddImmediateThumbT4(AddImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        rn = substring(instr, 19, 16)
        i = bit_at(instr, 26)
        setflags = False
        imm32 = chain(i, chain(imm3, imm8, 8), 11)
        if rd in (13, 15):
            print('unpredictable')
        else:
            return AddImmediateThumbT4(instr, setflags=setflags, d=rd, n=rn, imm32=imm32)
