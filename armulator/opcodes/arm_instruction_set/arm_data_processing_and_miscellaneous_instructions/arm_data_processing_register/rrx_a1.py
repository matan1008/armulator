from armulator.opcodes.abstract_opcodes.rrx import Rrx
from armulator.opcodes.opcode import Opcode


class RrxA1(Rrx, Opcode):
    def __init__(self, instruction, setflags, m, d):
        Opcode.__init__(self, instruction)
        Rrx.__init__(self, setflags, m, d)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        rd = instr[16:20]
        s = instr[11]
        return RrxA1(instr, **{"setflags": s, "m": rm.uint, "d": rd.uint})
