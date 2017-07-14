from armulator.armv6.opcodes.abstract_opcodes.push import Push
from armulator.armv6.opcodes.opcode import Opcode


class PushA1(Push, Opcode):
    def __init__(self, instruction, registers, unaligned_allowed):
        Opcode.__init__(self, instruction)
        Push.__init__(self, registers, unaligned_allowed)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[16:32]
        unaligned_allowed = False
        return PushA1(instr, **{"registers": register_list, "unaligned_allowed": unaligned_allowed})
