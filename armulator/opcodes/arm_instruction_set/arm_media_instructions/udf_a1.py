from armulator.opcodes.abstract_opcodes.udf import Udf
from armulator.opcodes.opcode import Opcode


class UdfA1(Udf, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Udf.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        return UdfA1(instr)
