from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.b import B


class BT3(B):
    @staticmethod
    def from_bitarray(instr, processor):
        imm11 = substring(instr, 10, 0)
        imm6 = substring(instr, 21, 16)
        j2 = bit_at(instr, 11)
        j1 = bit_at(instr, 13)
        s = bit_at(instr, 26)
        imm32 = chain(s, chain(j2, chain(j1, chain(imm6, imm11, 11), 17), 18), 19) << 1
        if processor.in_it_block():
            print('unpredictable')
        else:
            return BT3(instr, imm32=imm32)
