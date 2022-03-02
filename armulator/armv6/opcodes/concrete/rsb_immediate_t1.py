from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.rsb_immediate import RsbImmediate


class RsbImmediateT1(RsbImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 2, 0)
        rn = substring(instr, 5, 3)
        setflags = not processor.in_it_block()
        imm32 = 0
        return RsbImmediateT1(instr, setflags=setflags, d=rd, n=rn, imm32=imm32)
