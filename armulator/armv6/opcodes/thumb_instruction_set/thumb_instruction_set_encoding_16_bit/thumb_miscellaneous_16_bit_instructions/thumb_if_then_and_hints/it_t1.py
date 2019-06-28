from armulator.armv6.opcodes.abstract_opcodes.it import It
from armulator.armv6.opcodes.opcode import Opcode


class ItT1(It, Opcode):
    def __init__(self, instruction, firstcond, mask):
        Opcode.__init__(self, instruction)
        It.__init__(self, firstcond, mask)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        mask = instr[12:16]
        first_cond = instr[8:12]
        if first_cond == "0b1111" or (first_cond == "0b1110" and mask.count(1) != 1) or processor.in_it_block():
            print("unpredictable")
        else:
            return ItT1(instr, **{"firstcond": first_cond, "mask": mask})
