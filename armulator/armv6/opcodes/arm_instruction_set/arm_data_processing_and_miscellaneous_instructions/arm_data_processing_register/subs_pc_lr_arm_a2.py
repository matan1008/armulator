from armulator.armv6.opcodes.abstract_opcodes.subs_pc_lr_arm import SubsPcLrArm
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift


class SubsPcLrArmA2(SubsPcLrArm, Opcode):
    def __init__(self, instruction, n, opcode_, m, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        SubsPcLrArm.__init__(self, True, n, opcode_, m=m, shift_t=shift_t, shift_n=shift_n)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        type_o = instr[25:27]
        imm5 = instr[20:25]
        rn = instr[12:16]
        opcode_ = instr.bin[7:11]
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        return SubsPcLrArmA2(instr, **{"n": rn.uint, "opcode_": opcode_, "m": rm.uint,
                                       "shift_t": shift_t, "shift_n": shift_n})
