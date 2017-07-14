from armulator.armv6.opcodes.abstract_opcodes.lsl_register import LslRegister
from armulator.armv6.opcodes.opcode import Opcode


class LslRegisterT1(LslRegister, Opcode):
    def __init__(self, instruction, setflags, m, d, n):
        Opcode.__init__(self, instruction)
        LslRegister.__init__(self, setflags, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rdn = instr[13:16]
        rm = instr[10:13]
        setflags = not processor.in_it_block()
        return LslRegisterT1(instr, **{"setflags": setflags, "m": rm.uint, "d": rdn.uint, "n": rdn.uint})
