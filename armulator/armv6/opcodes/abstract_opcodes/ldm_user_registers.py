from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import add, sub, bit_at, bit_count
from armulator.armv6.opcodes.opcode import Opcode


class LdmUserRegisters(Opcode):
    def __init__(self, instruction, increment, word_higher, registers, n):
        super().__init__(instruction)
        self.increment = increment
        self.word_higher = word_higher
        self.registers = registers
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            elif processor.registers.current_mode_is_user_or_system():
                print('unpredictable')
            else:
                length = 4 * bit_count(self.registers, 1, 16)
                address = processor.registers.get(self.n) if self.increment else sub(processor.registers.get(self.n),
                                                                                     length, 32)
                if self.word_higher:
                    address = add(address, 4, 32)
                for i in range(15):
                    if bit_at(self.registers, i):
                        processor.registers.set_rmode(i, 0b10000, processor.mem_a_get(address, 4))
                        address = add(address, 4, 32)
