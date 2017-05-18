from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add_with_carry
from armulator.enums import InstrSet


class SubsPcLrThumb(AbstractOpcode):
    def __init__(self, imm32, n):
        super(SubsPcLrThumb, self).__init__()
        self.imm32 = imm32
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if (processor.core_registers.current_mode_is_user_or_system() or
                    processor.core_registers.current_instr_set() == InstrSet.InstrSet_ThumbEE):
                print "unpredictable"
            else:
                operand2 = self.imm32
                result = add_with_carry(processor.core_registers.get(self.n), ~operand2, "1")[0]
                if (processor.core_registers.CPSR[27:32] == "0b11010" and
                        processor.core_registers.get_cpsr_j() == "1" and
                        processor.core_registers.get_cpsr_t() == "1"):
                    print "unpredictable"
                else:
                    processor.branch_write_pc(result)
