from armulator.armv6.opcodes.abstract_opcodes.wfe import Wfe


class WfeA1(Wfe):
    @staticmethod
    def from_bitarray(instr, processor):
        return WfeA1(instr)
