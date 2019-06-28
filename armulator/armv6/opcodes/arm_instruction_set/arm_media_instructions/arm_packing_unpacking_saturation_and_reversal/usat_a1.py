from armulator.armv6.opcodes.abstract_opcodes.usat import Usat
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift


class UsatA1(Usat, Opcode):
    def __init__(self, instruction, saturate_to, d, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        Usat.__init__(self, saturate_to, d, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[28:32]
        sh = instr[25:26]
        imm5 = instr[20:25]
        rd = instr[16:20]
        sat_imm = instr[11:16]
        saturate_to = sat_imm.uint + 1
        shift_t, shift_n = decode_imm_shift(sh + "0b0", imm5)
        if rd.uint == 15 or rn.uint == 15:
            print("unpredictable")
        else:
            return UsatA1(instr, **{"saturate_to": saturate_to, "d": rd.uint, "n": rn.uint, "shift_t": shift_t,
                                    "shift_n": shift_n})
