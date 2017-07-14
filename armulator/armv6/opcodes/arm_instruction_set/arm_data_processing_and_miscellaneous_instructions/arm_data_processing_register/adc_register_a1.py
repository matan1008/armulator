from armulator.armv6.opcodes.abstract_opcodes.adc_register import AdcRegister
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift


class AdcRegisterA1(AdcRegister, Opcode):
    def __init__(self, instruction, setflags, m, d, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        AdcRegister.__init__(self, setflags, m, d, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        type_o = instr[25:27]
        imm5 = instr[20:25]
        rd = instr[16:20]
        rn = instr[12:16]
        s = instr[11]
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        return AdcRegisterA1(instr, **{"setflags": s, "m": rm.uint, "d": rd.uint, "n": rn.uint, "shift_t": shift_t,
                                       "shift_n": shift_n})
