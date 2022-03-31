from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.abstract_opcodes.subs_pc_lr_thumb import SubsPcLrThumb


class SubsPcLrThumbT1(SubsPcLrThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        n = 14
        imm32 = substring(instr, 7, 0)
        if processor.registers.current_mode_is_hyp():
            raise UndefinedInstructionException()
        elif ((processor.in_it_block() and not processor.last_in_it_block()) or
              processor.registers.current_instr_set() == InstrSet.THUMB_EE):
            print('unpredictable')
        else:
            return SubsPcLrThumbT1(instr, imm32=imm32, n=n)
