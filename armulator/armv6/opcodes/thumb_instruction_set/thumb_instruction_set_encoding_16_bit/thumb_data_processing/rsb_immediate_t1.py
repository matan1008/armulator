from armulator.armv6.opcodes.abstract_opcodes.rsb_immediate import RsbImmediate
from armulator.armv6.opcodes.opcode import Opcode
from bitstring import BitArray


class RsbImmediateT1(RsbImmediate, Opcode):
    def __init__(self, instruction, setflags, d, n, imm32):
        Opcode.__init__(self, instruction)
        RsbImmediate.__init__(self, setflags, d, n, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[13:16]
        rn = instr[10:13]
        setflags = not processor.in_it_block()
        imm32 = BitArray(length=32)
        return RsbImmediateT1(instr, **{"setflags": setflags, "d": rd.uint, "n": rn.uint, "imm32": imm32})
