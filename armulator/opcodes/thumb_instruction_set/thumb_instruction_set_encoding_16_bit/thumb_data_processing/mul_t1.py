from armulator.opcodes.abstract_opcodes.mul import Mul
from armulator.opcodes.opcode import Opcode
from armulator.configurations import ArchVersion


class MulT1(Mul, Opcode):
    def __init__(self, instruction, setflags, m, d, n):
        Opcode.__init__(self, instruction)
        Mul.__init__(self, setflags, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rdm = instr[13:16]
        rn = instr[10:13]
        setflags = not processor.in_it_block()
        if ArchVersion() < 6 and rdm.uint == rn.uint:
            print "unpredictable"
        else:
            return MulT1(instr, **{"setflags": setflags, "m": rdm.uint, "d": rdm.uint, "n": rn.uint})
