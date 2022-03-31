from armulator.armv6.opcodes.abstract_opcodes.yield_ import Yield


class YieldT2(Yield):
    @staticmethod
    def from_bitarray(instr, processor):
        return YieldT2(instr)
