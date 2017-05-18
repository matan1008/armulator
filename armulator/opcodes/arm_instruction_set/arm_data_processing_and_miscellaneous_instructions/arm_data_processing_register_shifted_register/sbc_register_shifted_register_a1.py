from armulator.opcodes.abstract_opcodes.sbc_register_shifted_register import SbcRegisterShiftedRegister
from armulator.opcodes.opcode import Opcode
from armulator.shift import decode_reg_shift


class SbcRegisterShiftedRegisterA1(SbcRegisterShiftedRegister, Opcode):
    def __init__(self, instruction, setflags, m, s, d, n, shift_t):
        Opcode.__init__(self, instruction)
        SbcRegisterShiftedRegister.__init__(self, setflags, m, s, d, n, shift_t)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        type_o = instr[25:27]
        rs = instr[20:24]
        rd = instr[16:20]
        rn = instr[12:16]
        s = instr[11]
        if rd == "0b1111" or rn == "0b1111" or rm == "0b1111" or rs == "0b1111":
            print "unpredictable"
        else:
            shift_t = decode_reg_shift(type_o)
            return SbcRegisterShiftedRegisterA1(instr, **{"setflags": s, "m": rm.uint, "s": rs.uint, "d": rd.uint,
                                                          "n": rn.uint, "shift_t": shift_t})
