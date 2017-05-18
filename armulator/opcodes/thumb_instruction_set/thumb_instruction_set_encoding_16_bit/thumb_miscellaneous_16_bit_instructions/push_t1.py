from armulator.opcodes.abstract_opcodes.push import Push
from armulator.opcodes.opcode import Opcode


class PushT1(Push, Opcode):
    def __init__(self, instruction, registers, unaligned_allowed):
        Opcode.__init__(self, instruction)
        Push.__init__(self, registers, unaligned_allowed)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        registers_list = instr[8:16]
        m = instr[7:8]
        registers = "0b0" + m + "0b000000" + registers_list
        unaligned_allowed = False
        if registers.count(1) < 1:
            print "unpredictable"
        else:
            return PushT1(instr, **{"registers": registers, "unaligned_allowed": unaligned_allowed})
