from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.msr_immediate_system import MsrImmediateSystem
from armulator.armv6.shift import arm_expand_imm


class MsrImmediateSystemA1(MsrImmediateSystem):
    @staticmethod
    def from_bitarray(instr, processor):
        mask = substring(instr, 19, 16)
        imm12 = substring(instr, 11, 0)
        write_spsr = bit_at(instr, 22)
        imm32 = arm_expand_imm(imm12)
        if mask == 0b0000:
            print('unpredictable')
        else:
            return MsrImmediateSystemA1(instr, write_spsr=write_spsr, mask=mask, imm32=imm32)
