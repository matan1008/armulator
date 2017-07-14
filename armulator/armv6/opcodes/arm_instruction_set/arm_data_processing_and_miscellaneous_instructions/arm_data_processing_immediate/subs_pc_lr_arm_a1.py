from armulator.armv6.opcodes.abstract_opcodes.subs_pc_lr_arm import SubsPcLrArm
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import arm_expand_imm


class SubsPcLrArmA1(SubsPcLrArm, Opcode):
    def __init__(self, instruction, n, opcode_, imm32):
        Opcode.__init__(self, instruction)
        SubsPcLrArm.__init__(self, False, n, opcode_, imm32=imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rn = instr[12:16]
        opcode = instr.bin[7:11]
        imm32 = arm_expand_imm(imm12)
        return SubsPcLrArmA1(instr, **{"n": rn.uint, "opcode_": opcode, "imm32": imm32})
