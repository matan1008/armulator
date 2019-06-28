from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add_with_carry
from armulator.armv6.enums import InstrSet


class SubsPcLrThumb(AbstractOpcode):
    def __init__(self, imm32, n):
        super(SubsPcLrThumb, self).__init__()
        self.imm32 = imm32
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if (processor.registers.current_mode_is_user_or_system() or
                    processor.registers.current_instr_set() == InstrSet.InstrSet_ThumbEE):
                print("unpredictable")
            else:
                operand2 = self.imm32
                result = add_with_carry(processor.registers.get(self.n), ~operand2, "1")[0]
                if (processor.registers.cpsr.get_m() == "0b11010" and
                        processor.registers.cpsr.get_j() and
                        processor.registers.cpsr.get_t()):
                    print("unpredictable")
                else:
                    processor.branch_write_pc(result)
