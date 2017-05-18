from armulator.opcodes.abstract_opcodes.mla import Mla
from armulator.opcodes.opcode import Opcode
from armulator.configurations import ArchVersion


class MlaA1(Mla, Opcode):
    def __init__(self, instruction, setflags, m, a, d, n):
        Opcode.__init__(self, instruction)
        Mla.__init__(self, setflags, m, a, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        rm = instr[20:24]
        ra = instr[16:20]
        rd = instr[12:16]
        setflags = instr[11]
        if rd.uint == 15 or rm.uint == 15 or rn.uint == 15 or ra.uint == 15 or (
                rn.uint == rd.uint and ArchVersion() < 6):
            print "unpredictable"
        else:
            return MlaA1(instr, **{"setflags": setflags, "m": rm.uint, "a": ra.uint, "d": rd.uint, "n": rn.uint})
