from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.abstract_opcodes.ldc_ldc2_literal import LdcLdc2Literal


class LdcLdc2LiteralT2(LdcLdc2Literal):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        coproc = substring(instr, 11, 8)
        add = bit_at(instr, 23)
        index = bit_at(instr, 24)
        imm32 = imm8 << 2
        if substring(instr, 23, 21) == 0b0000 or substring(coproc, 3, 1) == 0b101:
            raise UndefinedInstructionException()
        elif bit_at(instr, 21) or (not index and processor.registers.current_instr_set() != InstrSet.ARM):
            print('unpredictable')
        else:
            return LdcLdc2LiteralT2(instr, cp=coproc, add=add, imm32=imm32, index=index)
