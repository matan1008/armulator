from armulator.opcodes.abstract_opcodes.clrex import Clrex
from armulator.opcodes.opcode import Opcode


class ClrexA1(Clrex, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Clrex.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        return ClrexA1(instr)
