from armulator.armv6.opcodes.abstract_opcodes.mvn_register_shifted_register import MvnRegisterShiftedRegister
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_reg_shift


class MvnRegisterShiftedRegisterA1(MvnRegisterShiftedRegister, Opcode):
    def __init__(self, instruction, setflags, m, s, d, shift_t):
        Opcode.__init__(self, instruction)
        MvnRegisterShiftedRegister.__init__(self, setflags, m, s, d, shift_t)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        type_o = instr[25:27]
        rs = instr[20:24]
        rd = instr[16:20]
        s = instr[11]
        if rd == "0b1111" or rm == "0b1111" or rs == "0b1111":
            print("unpredictable")
        else:
            shift_t = decode_reg_shift(type_o)
            return MvnRegisterShiftedRegisterA1(instr, **{"setflags": s, "m": rm.uint, "s": rs.uint, "d": rd.uint,
                                                          "shift_t": shift_t})
