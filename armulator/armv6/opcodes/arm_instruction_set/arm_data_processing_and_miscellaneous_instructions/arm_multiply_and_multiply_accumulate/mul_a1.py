from armulator.armv6.opcodes.abstract_opcodes.mul import Mul
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.configurations import arch_version


class MulA1(Mul, Opcode):
    def __init__(self, instruction, setflags, m, d, n):
        Opcode.__init__(self, instruction)
        Mul.__init__(self, setflags, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        rm = instr[20:24]
        rd = instr[12:16]
        setflags = instr[11]
        if rd.uint == 15 or rm.uint == 15 or rn.uint == 15 or (rn.uint == rd.uint and arch_version() < 6):
            print "unpredictable"
        else:
            return MulA1(instr, **{"setflags": setflags, "m": rm.uint, "d": rd.uint, "n": rn.uint})
