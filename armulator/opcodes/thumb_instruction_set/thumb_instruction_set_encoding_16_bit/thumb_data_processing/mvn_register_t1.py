from armulator.opcodes.abstract_opcodes.mvn_register import MvnRegister
from armulator.opcodes.opcode import Opcode
from armulator.shift import SRType


class MvnRegisterT1(MvnRegister, Opcode):
    def __init__(self, instruction, setflags, m, d, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        MvnRegister.__init__(self, setflags, m, d, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[13:16]
        rm = instr[10:13]
        setflags = not processor.in_it_block()
        shift_t = SRType.SRType_LSL
        shift_n = 0
        return MvnRegisterT1(instr, **{"setflags": setflags, "m": rm.uint, "d": rd.uint,
                                       "shift_t": shift_t, "shift_n": shift_n})
