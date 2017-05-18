from armulator.opcodes.abstract_opcodes.ldrh_immediate_arm import LdrhImmediateArm
from armulator.opcodes.opcode import Opcode


class LdrhImmediateArmA1(LdrhImmediateArm, Opcode):
    def __init__(self, instruction, add, wback, index, imm32, t, n):
        Opcode.__init__(self, instruction)
        LdrhImmediateArm.__init__(self, add, wback, index, imm32, t, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        w = instr[10]
        p = instr[7]
        imm4_l = instr[-4:]
        imm4_h = instr[20:24]
        rt = instr[16:20]
        rn = instr[12:16]
        add = instr[8]
        imm32 = "0b000000000000000000000000" + imm4_h + imm4_l
        wback = (not p) or w
        if rt.uint == 15 or (wback and (rn.uint == 15 or rn.uint == rt.uint)):
            print "unpredictable"
        else:
            return LdrhImmediateArmA1(instr, **{"add": add, "wback": wback, "index": p, "imm32": imm32,
                                                "t": rt.uint, "n": rn.uint})
