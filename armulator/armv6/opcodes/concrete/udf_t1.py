from armulator.armv6.opcodes.abstract_opcodes.udf import Udf


class UdfT1(Udf):
    @staticmethod
    def from_bitarray(instr, processor):
        return UdfT1(instr)
