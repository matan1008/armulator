from armulator.armv6.opcodes.abstract_opcodes.mrrc import Mrrc
from armulator.armv6.opcodes.opcode import Opcode


class MrrcA1(Mrrc, Opcode):
    def __init__(self, instruction, cp, t, t2):
        Opcode.__init__(self, instruction)
        Mrrc.__init__(self, cp, t, t2)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        coproc = instr[20:24]
        rt = instr[16:20]
        rt2 = instr[12:16]
        if rt.uint == 15 or rt2.uint == 15 or rt.uint == rt2.uint:
            print("unpredictable")
        else:
            return MrrcA1(instr, **{"cp": coproc.uint, "t": rt.uint, "t2": rt2.uint})
