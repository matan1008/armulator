from armulator.armv6.opcodes.abstract_opcodes.usat import Usat
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift


class UsatT1(Usat, Opcode):
    def __init__(self, instruction, saturate_to, d, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        Usat.__init__(self, saturate_to, d, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        sat_imm = instr[27:32]
        imm2 = instr[24:26]
        rd = instr[20:24]
        imm3 = instr[17:20]
        rn = instr[12:16]
        sh = instr[10:11]
        saturate_to = sat_imm.uint + 1
        shift_t, shift_n = decode_imm_shift(sh + "0b0", imm3 + imm2)
        if rd.uint in (13, 15) or rn.uint in (13, 15):
            print("unpredictable")
        else:
            return UsatT1(instr, **{"saturate_to": saturate_to, "d": rd.uint, "n": rn.uint, "shift_t": shift_t,
                                    "shift_n": shift_n})
