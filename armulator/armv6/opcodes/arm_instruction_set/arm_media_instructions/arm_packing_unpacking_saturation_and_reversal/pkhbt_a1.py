from armulator.armv6.opcodes.abstract_opcodes.pkhbt import Pkhbt
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift


class PkhbtA1(Pkhbt, Opcode):
    def __init__(self, instruction, tb_form, m, d, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        Pkhbt.__init__(self, tb_form, m, d, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        tb = instr[25:26]
        imm5 = instr[20:25]
        rd = instr[16:20]
        rn = instr[12:16]
        tb_form = tb[0]
        shift_t, shift_n = decode_imm_shift(tb + "0b0", imm5)
        if rd.uint == 15 or rm.uint == 15 or rn.uint == 15:
            print("unpredictable")
        else:
            return PkhbtA1(instr, **{"tb_form": tb_form, "m": rm.uint, "d": rd.uint, "n": rn.uint, "shift_t": shift_t,
                                     "shift_n": shift_n})
