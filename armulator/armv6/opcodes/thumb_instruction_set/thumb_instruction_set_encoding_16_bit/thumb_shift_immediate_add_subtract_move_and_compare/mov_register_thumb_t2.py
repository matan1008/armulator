from armulator.armv6.opcodes.abstract_opcodes.mov_register_thumb import MovRegisterThumb
from armulator.armv6.opcodes.opcode import Opcode


class MovRegisterThumbT2(MovRegisterThumb, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        MovRegisterThumb.__init__(self, True, m, d)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[13:16]
        rm = instr[10:13]
        if processor.in_it_block():
            print "unpredictable"
        else:
            return MovRegisterThumbT2(instr, **{"m": rm.uint, "d": rd.uint})
