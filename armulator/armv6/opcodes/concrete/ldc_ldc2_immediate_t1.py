from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldc_ldc2_immediate import LdcLdc2Immediate


class LdcLdc2ImmediateT1(LdcLdc2Immediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        coproc = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        wback = bit_at(instr, 21)
        add = bit_at(instr, 23)
        index = bit_at(instr, 24)
        imm32 = imm8 << 2
        if substring(instr, 24, 21) == 0b0000:
            raise UndefinedInstructionException()
        else:
            return LdcLdc2ImmediateT1(instr, cp=coproc, n=rn, add=add, imm32=imm32, index=index, wback=wback)
