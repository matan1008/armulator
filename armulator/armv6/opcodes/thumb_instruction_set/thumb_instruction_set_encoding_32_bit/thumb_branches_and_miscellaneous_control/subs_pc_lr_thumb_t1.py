from armulator.armv6.opcodes.abstract_opcodes.subs_pc_lr_thumb import SubsPcLrThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend
from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.enums import InstrSet


class SubsPcLrThumbT1(SubsPcLrThumb, Opcode):
    def __init__(self, instruction, imm32, n):
        Opcode.__init__(self, instruction)
        SubsPcLrThumb.__init__(self, imm32, n)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        n = 14
        imm8 = instr[24:32]
        imm32 = zero_extend(imm8, 32)
        if processor.registers.current_mode_is_hyp():
            raise UndefinedInstructionException()
        elif ((processor.in_it_block() and not processor.last_in_it_block()) or
              processor.registers.current_instr_set() == InstrSet.InstrSet_ThumbEE):
            print "unpredictable"
        else:
            return SubsPcLrThumbT1(instr, **{"imm32": imm32, "n": n})
