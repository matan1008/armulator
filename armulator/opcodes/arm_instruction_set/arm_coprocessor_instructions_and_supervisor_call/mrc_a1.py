from armulator.opcodes.abstract_opcodes.mrc import Mrc
from armulator.opcodes.opcode import Opcode


class MrcA1(Mrc, Opcode):
    def __init__(self, instruction, cp, t):
        Opcode.__init__(self, instruction)
        Mrc.__init__(self, cp, t)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        coproc = instr[20:24]
        rt = instr[16:20]
        return MrcA1(instr, **{"cp": coproc.uint, "t": rt.uint})
