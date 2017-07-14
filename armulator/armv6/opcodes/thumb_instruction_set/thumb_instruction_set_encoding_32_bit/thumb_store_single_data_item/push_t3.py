from armulator.armv6.opcodes.abstract_opcodes.push import Push
from armulator.armv6.opcodes.opcode import Opcode
from bitstring import BitArray


class PushT3(Push, Opcode):
    def __init__(self, instruction, registers, unaligned_allowed):
        Opcode.__init__(self, instruction)
        Push.__init__(self, registers, unaligned_allowed)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[16:20]
        registers = BitArray(length=16)
        registers[15 - rt.uint] = True
        unaligned_allowed = True
        if rt.uint in (13, 15):
            print "unpredictable"
        else:
            return PushT3(instr, **{"registers": registers, "unaligned_allowed": unaligned_allowed})
