from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldc_ldc2_literal import LdcLdc2Literal


class LdcLdc2LiteralA2(LdcLdc2Literal):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        coproc = substring(instr, 11, 8)
        index = bit_at(instr, 24)
        add = bit_at(instr, 23)
        wback = bit_at(instr, 21)
        if substring(coproc, 3, 1) == 0b101:
            raise UndefinedInstructionException()
        elif wback:
            print('unpredictable')
        else:
            imm32 = imm8 << 2
            return LdcLdc2LiteralA2(instr, cp=coproc, add=add, imm32=imm32, index=index)
