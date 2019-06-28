from armulator.armv6.opcodes.abstract_opcodes.mov_register_thumb import MovRegisterThumb
from armulator.armv6.opcodes.opcode import Opcode


class MovRegisterThumbT3(MovRegisterThumb, Opcode):
    def __init__(self, instruction, setflags, m, d):
        Opcode.__init__(self, instruction)
        MovRegisterThumb.__init__(self, setflags, m, d)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        setflags = instr[11]
        if (setflags and (rd.uint in (13, 15) or rm.uint in (13, 15))) or (
                    not setflags and (rd.uint == 15 or rm.uint == 15 or (rd.uint == 13 and rm.uint == 13))):
            print("unpredictable")
        else:
            return MovRegisterThumbT3(instr, **{"setflags": setflags, "m": rm.uint, "d": rd.uint})
