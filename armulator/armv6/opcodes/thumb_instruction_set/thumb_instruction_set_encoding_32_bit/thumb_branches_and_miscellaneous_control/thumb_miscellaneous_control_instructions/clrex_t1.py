from armulator.armv6.opcodes.abstract_opcodes.clrex import Clrex
from armulator.armv6.opcodes.opcode import Opcode


class ClrexT1(Clrex, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Clrex.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        return ClrexT1(instr)
