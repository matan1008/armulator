from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import add, sub, bit_count, bit_at
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.opcode import Opcode


class LdmExceptionReturn(Opcode):
    def __init__(self, instruction, increment, word_higher, wback, registers, n):
        super().__init__(instruction)
        self.increment = increment
        self.word_higher = word_higher
        self.wback = wback
        self.registers = registers
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            elif (processor.registers.current_mode_is_user_or_system() or
                  processor.registers.current_instr_set() == InstrSet.THUMB_EE):
                print('unpredictable')
            else:
                length = (4 * bit_count(self.registers, 1, 16)) + 4
                address = processor.registers.get(self.n) if self.increment else sub(processor.registers.get(self.n),
                                                                                     length, 32)
                if self.word_higher:
                    address = add(address, 4, 32)
                for i in range(15):
                    if bit_at(self.registers, i):
                        processor.registers.set(i, processor.mem_a_get(address, 4))
                        address = add(address, 4, 32)
                new_pc_value = processor.mem_a_get(address, 4)
                if self.wback and not bit_at(self.registers, self.n):
                    processor.registers.set(
                        self.n,
                        (add(processor.registers.get(self.n), length, 32)
                         if self.increment else sub(processor.registers.get(self.n), length, 32))
                    )
                if self.wback and bit_at(self.registers, self.n):
                    processor.registers.set(self.n, 0x00000000)  # unknown
                processor.registers.cpsr_write_by_instr(processor.registers.get_spsr(), 0b1111, True)
                if processor.registers.cpsr.m == 0b11010 and processor.registers.cpsr.j and processor.registers.cpsr.t:
                    print('unpredictable')
                else:
                    processor.branch_write_pc(new_pc_value)
