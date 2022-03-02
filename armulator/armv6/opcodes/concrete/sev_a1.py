from armulator.armv6.opcodes.abstract_opcodes.sev import Sev


class SevA1(Sev):
    @staticmethod
    def from_bitarray(instr, processor):
        return SevA1(instr)
