from armulator.armv6.opcodes.abstract_opcodes.bxj import Bxj
from armulator.armv6.opcodes.opcode import Opcode


class BxjT1(Bxj, Opcode):
    def __init__(self, instruction, m):
        Opcode.__init__(self, instruction)
        Bxj.__init__(self, m)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[12:16]
        if rm.uint in (13, 15) or (processor.in_it_block() and not processor.last_in_it_block()):
            print("unpredictable")
        else:
            return BxjT1(instr, **{"m": rm.uint})
