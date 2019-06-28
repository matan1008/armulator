from armulator.armv6.opcodes.abstract_opcodes.rrx import Rrx
from armulator.armv6.opcodes.opcode import Opcode


class RrxT1(Rrx, Opcode):
    def __init__(self, instruction, setflags, m, d):
        Opcode.__init__(self, instruction)
        Rrx.__init__(self, setflags, m, d)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        setflags = instr[11]
        if rd.uint in (13, 15) or rm.uint in (13, 15):
            print("unpredictable")
        else:
            return RrxT1(instr, **{"setflags": setflags, "m": rm.uint, "d": rd.uint})
