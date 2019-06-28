from armulator.armv6.opcodes.abstract_opcodes.push import Push
from armulator.armv6.opcodes.opcode import Opcode


class PushT2(Push, Opcode):
    def __init__(self, instruction, registers, unaligned_allowed):
        Opcode.__init__(self, instruction)
        Push.__init__(self, registers, unaligned_allowed)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[19:32]
        m = instr[17:18]
        unaligned_allowed = True
        registers = "0b0" + m + "0b0" + register_list
        if registers.count(1) < 2:
            print("unpredictable")
        else:
            return PushT2(instr, **{"registers": registers, "unaligned_allowed": unaligned_allowed})
