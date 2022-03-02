from armulator.armv6.bits_ops import lower_chunk
from armulator.armv6.opcodes.abstract_opcodes.svc import Svc


class SvcA1(Svc):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = lower_chunk(instr, 24)
        return SvcA1(instr, imm32=imm32)
