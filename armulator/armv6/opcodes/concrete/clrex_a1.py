from armulator.armv6.opcodes.abstract_opcodes.clrex import Clrex


class ClrexA1(Clrex):
    @staticmethod
    def from_bitarray(instr, processor):
        return ClrexA1(instr)
