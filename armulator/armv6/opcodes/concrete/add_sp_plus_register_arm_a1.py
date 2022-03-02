from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.add_sp_plus_register_arm import AddSpPlusRegisterArm
from armulator.armv6.shift import decode_imm_shift


class AddSpPlusRegisterArmA1(AddSpPlusRegisterArm):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 6, 5)
        imm5 = substring(instr, 11, 7)
        rd = substring(instr, 15, 12)
        s = bit_at(instr, 20)
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        return AddSpPlusRegisterArmA1(instr, setflags=s, m=rm, d=rd, shift_t=shift_t, shift_n=shift_n)
