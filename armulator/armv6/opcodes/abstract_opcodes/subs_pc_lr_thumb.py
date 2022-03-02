from armulator.armv6.bits_ops import add_with_carry, bit_not
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.opcode import Opcode


class SubsPcLrThumb(Opcode):
    def __init__(self, instruction, imm32, n):
        super().__init__(instruction)
        self.imm32 = imm32
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if (processor.registers.current_mode_is_user_or_system() or
                    processor.registers.current_instr_set() == InstrSet.THUMB_EE):
                print('unpredictable')
            else:
                operand2 = self.imm32
                result = add_with_carry(processor.registers.get(self.n), bit_not(operand2, 32), 1)[0]
                if (processor.registers.cpsr.m == 0b11010 and
                        processor.registers.cpsr.j and
                        processor.registers.cpsr.t):
                    print('unpredictable')
                else:
                    processor.branch_write_pc(result)
