from armulator.armv6.opcodes.abstract_opcodes.bx import Bx
from armulator.armv6.opcodes.opcode import Opcode


class BxT1(Bx, Opcode):
    def __init__(self, instruction, m):
        Opcode.__init__(self, instruction)
        Bx.__init__(self, m)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[9:13]
        if processor.in_it_block() and not processor.last_in_it_block():
            print("unpredictable")
        else:
            return BxT1(instr, **{"m": rm.uint})
