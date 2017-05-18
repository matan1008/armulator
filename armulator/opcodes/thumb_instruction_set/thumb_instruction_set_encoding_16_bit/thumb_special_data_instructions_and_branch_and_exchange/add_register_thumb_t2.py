from armulator.opcodes.abstract_opcodes.add_register_thumb import AddRegisterThumb
from armulator.opcodes.opcode import Opcode
from armulator.shift import SRType


class AddRegisterThumbT2(AddRegisterThumb, Opcode):
    def __init__(self, instruction, setflags, m, d, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        AddRegisterThumb.__init__(self, setflags, m, d, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rdn = instr[8:9] + instr[13:16]
        rm = instr[9:13]
        setflags = False
        shift_t = SRType.SRType_LSL
        shift_n = 0
        if (rdn.uint == 15 and rm.uint == 15) or (
                            rdn.uint == 15 and processor.in_it_block() and not processor.last_in_it_block()):
            print "unpredictable"
        else:
            return AddRegisterThumbT2(instr, **{"setflags": setflags, "m": rm.uint, "d": rdn.uint, "n": rdn.uint,
                                                "shift_t": shift_t, "shift_n": shift_n})
