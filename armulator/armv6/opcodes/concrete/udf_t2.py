from armulator.armv6.opcodes.abstract_opcodes.udf import Udf


class UdfT2(Udf):
    @staticmethod
    def from_bitarray(instr, processor):
        return UdfT2(instr)
