from armulator.armv6.opcodes.abstract_opcodes.revsh import Revsh
from armulator.armv6.opcodes.opcode import Opcode


class RevshT1(Revsh, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        Revsh.__init__(self, m, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[13:16]
        rm = instr[10:13]
        return RevshT1(instr, **{"m": rm.uint, "d": rd.uint})
