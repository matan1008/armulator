from armulator.opcodes.abstract_opcodes.mov_register_thumb import MovRegisterThumb
from armulator.opcodes.opcode import Opcode


class MovRegisterThumbT1(MovRegisterThumb, Opcode):
    def __init__(self, instruction, setflags, m, d):
        Opcode.__init__(self, instruction)
        MovRegisterThumb.__init__(self, setflags, m, d)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[8:9] + instr[13:16]
        rm = instr[9:13]
        setflags = False
        if rd.uint == 15 and processor.in_it_block() and not processor.last_in_it_block():
            print "unpredictable"
        else:
            return MovRegisterThumbT1(instr, **{"setflags": setflags, "m": rm.uint, "d": rd.uint})
