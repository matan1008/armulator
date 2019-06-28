from armulator.armv6.opcodes.abstract_opcodes.pkhbt import Pkhbt
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class PkhbtT1(Pkhbt, Opcode):
    def __init__(self, instruction, tb_form, m, d, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        Pkhbt.__init__(self, tb_form, m, d, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        tbform = instr[26]
        t = instr[27]
        imm2 = instr[24:26]
        rd = instr[20:24]
        imm3 = instr[17:20]
        rn = instr[12:16]
        s = instr[11]
        shift_t, shift_n = decode_imm_shift(instr[26:27] + "0b0", imm3 + imm2)
        if s or t:
            raise UndefinedInstructionException()
        elif rn.uint in (13, 15) or rm.uint in (13, 15) or rd.uint in (13, 15):
            print("unpredictable")
        else:
            return PkhbtT1(instr, **{"tb_form": tbform, "m": rm.uint, "d": rd.uint, "n": rn.uint, "shift_t": shift_t,
                                     "shift_n": shift_n})
