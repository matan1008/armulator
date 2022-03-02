from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.tst_immediate import TstImmediate
from armulator.armv6.shift import thumb_expand_imm_c


class TstImmediateT1(TstImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        imm3 = substring(instr, 14, 12)
        rn = substring(instr, 19, 16)
        i = bit_at(instr, 26)
        imm32, carry = thumb_expand_imm_c(chain(i, chain(imm3, imm8, 8), 11), processor.registers.cpsr.c)
        if rn in (13, 15):
            print('unpredictable')
        else:
            return TstImmediateT1(instr, n=rn, imm32=imm32, carry=carry)
