from armulator.armv6.opcodes.abstract_opcodes.wfi import Wfi


class WfiA1(Wfi):
    @staticmethod
    def from_bitarray(instr, processor):
        return WfiA1(instr)
