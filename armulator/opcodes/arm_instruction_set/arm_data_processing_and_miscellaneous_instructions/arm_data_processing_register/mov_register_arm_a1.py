from armulator.opcodes.abstract_opcodes.mov_register_arm import MovRegisterArm
from armulator.opcodes.opcode import Opcode


class MovRegisterArmA1(MovRegisterArm, Opcode):
    def __init__(self, instruction, setflags, m, d):
        Opcode.__init__(self, instruction)
        MovRegisterArm.__init__(self, setflags, m, d)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        rd = instr[16:20]
        s = instr[11]
        return MovRegisterArmA1(instr, **{"setflags": s, "m": rm.uint, "d": rd.uint})
