from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldr_literal import LdrLiteral


class LdrLiteralT2(LdrLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 11, 0)
        rt = substring(instr, 15, 12)
        add = bit_at(instr, 23)
        if rt == 15 and processor.in_it_block() and not processor.last_in_it_block():
            print('unpredictable')
        else:
            return LdrLiteralT2(instr, add=add, imm32=imm32, t=rt)
