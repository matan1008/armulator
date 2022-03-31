from armulator.armv6.opcodes.abstract_opcodes.wfi import Wfi


class WfiT2(Wfi):
    @staticmethod
    def from_bitarray(instr, processor):
        return WfiT2(instr)
