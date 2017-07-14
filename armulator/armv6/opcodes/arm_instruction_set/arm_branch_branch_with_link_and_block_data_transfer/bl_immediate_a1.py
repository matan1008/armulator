from armulator.armv6.opcodes.abstract_opcodes.bl_immediate import BlImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import sign_extend
from armulator.armv6.enums import InstrSet


class BlImmediateA1(BlImmediate, Opcode):
    def __init__(self, instruction, target_instr_set, imm32):
        Opcode.__init__(self, instruction)
        BlImmediate.__init__(self, target_instr_set, imm32)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = sign_extend(instr[8:32] + "0b00", 32)
        return BlImmediateA1(instr, **{"target_instr_set": InstrSet.InstrSet_ARM, "imm32": imm32})
