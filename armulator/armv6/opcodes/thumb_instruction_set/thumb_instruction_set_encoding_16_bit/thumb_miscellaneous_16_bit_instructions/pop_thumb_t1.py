from armulator.armv6.opcodes.abstract_opcodes.pop_thumb import PopThumb
from armulator.armv6.opcodes.opcode import Opcode


class PopThumbT1(PopThumb, Opcode):
    def __init__(self, instruction, registers, unaligned_allowed):
        Opcode.__init__(self, instruction)
        PopThumb.__init__(self, registers, unaligned_allowed)

    def is_pc_changing_opcode(self):
        return self.registers[0]

    @staticmethod
    def from_bitarray(instr, processor):
        unaligned_allowed = False
        registers_list = instr[8:16]
        p = instr[7:8]
        registers = p + "0b0000000" + registers_list
        if registers.count(1) < 1 or (registers[0] and processor.in_it_block() and not processor.last_in_it_block()):
            print "unpredictable"
        else:
            return PopThumbT1(instr, **{"registers": registers, "unaligned_allowed": unaligned_allowed})
