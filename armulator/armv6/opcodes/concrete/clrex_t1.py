from armulator.armv6.opcodes.abstract_opcodes.clrex import Clrex


class ClrexT1(Clrex):
    @staticmethod
    def from_bitarray(instr, processor):
        return ClrexT1(instr)
