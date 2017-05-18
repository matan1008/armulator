from armulator.opcodes.abstract_opcodes.bl_immediate import BlImmediate
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import sign_extend
from armulator.enums import InstrSet


class BlImmediateA2(BlImmediate, Opcode):
    def __init__(self, instruction, target_instr_set, imm32):
        Opcode.__init__(self, instruction)
        BlImmediate.__init__(self, target_instr_set, imm32)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        imm24 = instr[8:32]
        imm32 = sign_extend(imm24 + instr[7:8] + "0b0", 32)
        target_instrset = InstrSet.InstrSet_Thumb
        return BlImmediateA2(instr, **{"target_instr_set": target_instrset, "imm32": imm32})
