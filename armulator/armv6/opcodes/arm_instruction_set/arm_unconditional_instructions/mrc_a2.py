from armulator.armv6.opcodes.abstract_opcodes.mrc import Mrc
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class MrcA2(Mrc, Opcode):
    def __init__(self, instruction, cp, t):
        Opcode.__init__(self, instruction)
        Mrc.__init__(self, cp, t)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        coproc = instr[20:24]
        rt = instr[16:20]
        if coproc[0:3] == "0b101":
            raise UndefinedInstructionException()
        else:
            return MrcA2(instr, **{"cp": coproc.uint, "t": rt.uint})
