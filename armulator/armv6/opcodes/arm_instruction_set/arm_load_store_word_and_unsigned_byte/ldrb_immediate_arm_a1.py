from armulator.armv6.opcodes.abstract_opcodes.ldrb_immediate_arm import LdrbImmediateArm
from armulator.armv6.opcodes.opcode import Opcode


class LdrbImmediateArmA1(LdrbImmediateArm, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        LdrbImmediateArm.__init__(self, add, wback, index, t, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        index = instr[7]
        add = instr[8]
        w = instr[10]
        imm12 = instr[20:32]
        rt = instr[16:20]
        rn = instr[12:16]
        wback = (not index) or w
        imm32 = "0b00000000000000000000" + imm12
        if rt.uint == 15 or (wback and rn.uint == rt.uint):
            print("unpredictable")
        else:
            return LdrbImmediateArmA1(instr, **{"add": add, "wback": wback, "index": index, "t": rt.uint, "n": rn.uint,
                                                "imm32": imm32})
