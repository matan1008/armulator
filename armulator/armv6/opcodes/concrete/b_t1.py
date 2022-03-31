from armulator.armv6.bits_ops import substring, to_signed
from armulator.armv6.opcodes.abstract_opcodes.b import B


class BT1(B):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        imm32 = to_signed(imm8 * 2, 9)
        if processor.in_it_block():
            print('unpredictable')
        else:
            return BT1(instr, imm32=imm32)
