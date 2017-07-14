from armulator.armv6.opcodes.abstract_opcodes.yield_ import Yield
from armulator.armv6.opcodes.opcode import Opcode


class YieldT1(Yield, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Yield.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        return YieldT1(instr)
