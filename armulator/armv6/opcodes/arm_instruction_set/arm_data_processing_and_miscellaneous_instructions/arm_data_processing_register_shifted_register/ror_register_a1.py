from armulator.armv6.opcodes.abstract_opcodes.ror_register import RorRegister
from armulator.armv6.opcodes.opcode import Opcode


class RorRegisterA1(RorRegister, Opcode):
    def __init__(self, instruction, setflags, m, d, n):
        Opcode.__init__(self, instruction)
        RorRegister.__init__(self, setflags, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        rm = instr[20:24]
        rd = instr[16:20]
        s = instr[11]
        if rd == "0b1111" or rn == "0b1111" or rm == "0b1111":
            print("unpredictable")
        else:
            return RorRegisterA1(instr, **{"setflags": s, "m": rm.uint, "d": rd.uint,
                                           "n": rn.uint})
