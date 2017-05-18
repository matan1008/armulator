from armulator.opcodes.abstract_opcodes.mcrr import Mcrr
from armulator.opcodes.opcode import Opcode
from armulator.arm_exceptions import UndefinedInstructionException


class McrrA2(Mcrr, Opcode):
    def __init__(self, instruction, cp, t, t2):
        Opcode.__init__(self, instruction)
        Mcrr.__init__(self, cp, t, t2)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        coproc = instr[20:24]
        rt = instr[16:20]
        rt2 = instr[12:16]
        if coproc[0:3] == "0b101":
            raise UndefinedInstructionException()
        elif rt.uint == 15 or rt2.uint == 15:
            print "unpredictable"
        else:
            return McrrA2(instr, **{"cp": coproc.uint, "t": rt.uint, "t2": rt2.uint})
