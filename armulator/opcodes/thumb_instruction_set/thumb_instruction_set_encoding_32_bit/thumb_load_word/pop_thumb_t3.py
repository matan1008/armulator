from armulator.opcodes.abstract_opcodes.pop_thumb import PopThumb
from armulator.opcodes.opcode import Opcode
from bitstring import BitArray


class PopThumbT3(PopThumb, Opcode):
    def __init__(self, instruction, registers, unaligned_allowed):
        Opcode.__init__(self, instruction)
        PopThumb.__init__(self, registers, unaligned_allowed)

    def is_pc_changing_opcode(self):
        return self.registers[0]

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[16:20]
        registers = BitArray(length=16)
        registers[15 - rt.uint] = True
        unaligned_allowed = True
        if rt.uint == 13 or (rt.uint == 15 and processor.in_it_block() and not processor.last_in_it_block()):
            print "unpredictable"
        else:
            return PopThumbT3(instr, **{"registers": registers, "unaligned_allowed": unaligned_allowed})
