from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.msr_immediate_application import MsrImmediateApplication
from armulator.armv6.shift import arm_expand_imm


class MsrImmediateApplicationA1(MsrImmediateApplication):
    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = substring(instr, 11, 0)
        imm32 = arm_expand_imm(imm12)
        mask = substring(instr, 19, 18)
        write_nzcvq = bit_at(mask, 1)
        write_g = bit_at(mask, 0)
        return MsrImmediateApplicationA1(instr, write_nzcvq=write_nzcvq, write_g=write_g, imm32=imm32)
