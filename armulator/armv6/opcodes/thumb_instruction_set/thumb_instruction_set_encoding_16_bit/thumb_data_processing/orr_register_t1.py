from armulator.armv6.opcodes.abstract_opcodes.orr_register import OrrRegister
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import SRType


class OrrRegisterT1(OrrRegister, Opcode):
    def __init__(self, instruction, setflags, m, d, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        OrrRegister.__init__(self, setflags, m, d, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rdn = instr[13:16]
        rm = instr[10:13]
        setflags = not processor.in_it_block()
        shift_t = SRType.SRType_LSL
        shift_n = 0
        return OrrRegisterT1(instr, **{"setflags": setflags, "m": rm.uint, "d": rdn.uint, "n": rdn.uint,
                                       "shift_t": shift_t, "shift_n": shift_n})
