from armulator.armv6.opcodes.abstract_opcodes.add_register_shifted_register import AddRegisterShiftedRegister
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_reg_shift


class AddRegisterShiftedRegisterA1(AddRegisterShiftedRegister, Opcode):
    def __init__(self, instruction, setflags, m, s, d, n, shift_t):
        Opcode.__init__(self, instruction)
        AddRegisterShiftedRegister.__init__(self, setflags, m, s, d, n, shift_t)

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
            return AddRegisterShiftedRegisterA1(instr, **{"setflags": s, "m": rm.uint, "s": rs.uint, "d": rd.uint,
                                                          "n": rn.uint, "shift_t": shift_t})
