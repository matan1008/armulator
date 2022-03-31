from armulator.armv6.opcodes.abstract_opcodes.sev import Sev


class SevT1(Sev):
    @staticmethod
    def from_bitarray(instr, processor):
        return SevT1(instr)
