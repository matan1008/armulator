from armulator.armv6.opcodes.abstract_opcodes.mvn_register import MvnRegister
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift


class MvnRegisterT2(MvnRegister, Opcode):
    def __init__(self, instruction, setflags, m, d, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        MvnRegister.__init__(self, setflags, m, d, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        type_o = instr[26:28]
        imm2 = instr[24:26]
        rd = instr[20:24]
        imm3 = instr[17:20]
        setflags = instr[11]
        shift_t, shift_n = decode_imm_shift(type_o, imm3 + imm2)
        if rd.uint in (13, 15) or rm.uint in (13, 15):
            print "unpredictable"
        else:
            return MvnRegisterT2(instr, **{"setflags": setflags, "m": rm.uint, "d": rd.uint, "shift_t": shift_t,
                                           "shift_n": shift_n})
