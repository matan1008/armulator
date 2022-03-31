from armulator.armv6.opcodes.abstract_opcodes.wfe import Wfe


class WfeT1(Wfe):
    @staticmethod
    def from_bitarray(instr, processor):
        return WfeT1(instr)
