from armulator.armv6.opcodes.abstract_opcodes.udf import Udf


class UdfA1(Udf):
    @staticmethod
    def from_bitarray(instr, processor):
        return UdfA1(instr)
