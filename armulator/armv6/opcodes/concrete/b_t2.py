from armulator.armv6.bits_ops import substring, sign_extend
from armulator.armv6.opcodes.abstract_opcodes.b import B


class BT2(B):
    @staticmethod
    def from_bitarray(instr, processor):
        imm11 = substring(instr, 10, 0)
        imm32 = sign_extend(imm11 * 2, 12, 32)
        if processor.in_it_block() and not processor.last_in_it_block():
            print('unpredictable')
        else:
            return BT2(instr, imm32=imm32)
