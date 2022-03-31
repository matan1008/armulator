from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import add, sub
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.opcode import Opcode


class Rfe(Opcode):
    def __init__(self, instruction, increment, word_higher, wback, n):
        super().__init__(instruction)
        self.increment = increment
        self.word_higher = word_higher
        self.wback = wback
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            elif (not processor.registers.current_mode_is_not_user() or
                  processor.registers.current_instr_set() == InstrSet.THUMB_EE):
                print('unpredictable')
            else:
                address = (processor.registers.get(self.n)
                           if self.increment else sub(processor.registers.get(self.n), 8, 32))
                if self.word_higher:
                    address = add(address, 4, 32)
                new_pc_value = processor.mem_a_get(address, 4)
                spsr_value = processor.mem_a_get(add(address, 4, 32), 4)
                if self.wback:
                    processor.registers.set(
                        self.n,
                        (add(processor.registers.get(self.n), 8, 32)
                         if self.increment else sub(processor.registers.get(self.n), 8, 32))
                    )
                processor.registers.cpsr_write_by_instr(spsr_value, 0b1111, True)
                if (processor.registers.cpsr.m == 0b11010 and
                        processor.registers.cpsr.j and
                        processor.registers.cpsr.t):
                    print('unpredictable')
                else:
                    processor.branch_write_pc(new_pc_value)
