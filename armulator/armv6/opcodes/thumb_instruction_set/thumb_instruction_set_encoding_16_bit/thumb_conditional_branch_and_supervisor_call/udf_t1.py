from armulator.armv6.opcodes.abstract_opcodes.udf import Udf
from armulator.armv6.opcodes.opcode import Opcode


class UdfT1(Udf, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Udf.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        return UdfT1(instr)
