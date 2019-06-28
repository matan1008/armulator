from armulator.armv6.opcodes.abstract_opcodes.mrs_application import MrsApplication
from armulator.armv6.opcodes.opcode import Opcode


class MrsApplicationT1(MrsApplication, Opcode):
    def __init__(self, instruction, d):
        Opcode.__init__(self, instruction)
        MrsApplication.__init__(self, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[20:24]
        if rd.uint in (13, 15):
            print("unpredictable")
        else:
            return MrsApplicationT1(instr, **{"d": rd.uint})
