from armulator.armv6.opcodes.abstract_opcodes.yield_ import Yield


class YieldA1(Yield):
    @staticmethod
    def from_bitarray(instr, processor):
        return YieldA1(instr)
