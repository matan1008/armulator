from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.mvn_immediate import MvnImmediate
from armulator.armv6.shift import thumb_expand_imm_c


class MvnImmediateT1(MvnImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        setflags = bit_at(instr, 20)
        i = bit_at(instr, 26)
        imm32, carry = thumb_expand_imm_c(chain(i, chain(imm3, imm8, 8), 11), processor.registers.cpsr.c)
        if rd in (13, 15):
            print('unpredictable')
        else:
            return MvnImmediateT1(instr, setflags=setflags, d=rd, imm32=imm32, carry=carry)
