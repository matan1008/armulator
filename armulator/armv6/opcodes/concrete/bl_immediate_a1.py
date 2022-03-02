from armulator.armv6.bits_ops import sign_extend, substring
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.abstract_opcodes.bl_blx_immediate import BlBlxImmediate


class BlBlxImmediateA1(BlBlxImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = sign_extend(substring(instr, 23, 0) << 2, 26, 32)
        return BlBlxImmediateA1(instr, target_instr_set=InstrSet.ARM, imm32=imm32)
