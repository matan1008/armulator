from armulator.armv6.opcodes.abstract_opcodes.yield_ import Yield


class YieldT1(Yield):
    @staticmethod
    def from_bitarray(instr, processor):
        return YieldT1(instr)
