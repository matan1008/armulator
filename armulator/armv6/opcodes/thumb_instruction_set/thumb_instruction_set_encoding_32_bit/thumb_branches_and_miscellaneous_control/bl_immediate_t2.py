from armulator.armv6.opcodes.abstract_opcodes.bl_immediate import BlImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import sign_extend
from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.enums import InstrSet


class BlImmediateT2(BlImmediate, Opcode):
    def __init__(self, instruction, target_instr_set, imm32):
        Opcode.__init__(self, instruction)
        BlImmediate.__init__(self, target_instr_set, imm32)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        h = instr[31]
        imm10l = instr[21:31]
        j2 = instr[20:21]
        j1 = instr[18:19]
        imm10h = instr[6:16]
        s = instr[5:6]
        i1 = ~(j1 ^ s)
        i2 = ~(j2 ^ s)
        imm32 = sign_extend(s + i1 + i2 + imm10h + imm10l + "0b00", 32)
        target_instr_set = InstrSet.InstrSet_ARM
        if processor.registers.current_instr_set() == InstrSet.InstrSet_ThumbEE or h:
            raise UndefinedInstructionException()
        elif processor.in_it_block() and not processor.last_in_it_block():
            print "unpredictable"
        else:
            return BlImmediateT2(instr, **{"target_instr_set": target_instr_set, "imm32": imm32})
