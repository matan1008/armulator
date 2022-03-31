from armulator.armv6.opcodes.abstract_opcodes.wfe import Wfe


class WfeT2(Wfe):
    @staticmethod
    def from_bitarray(instr, processor):
        return WfeT2(instr)
