from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add, sub
from bitstring import BitArray
from armulator.arm_exceptions import UndefinedInstructionException


class StmUserRegisters(AbstractOpcode):
    def __init__(self, increment, word_higher, registers, n):
        super(StmUserRegisters, self).__init__()
        self.increment = increment
        self.word_higher = word_higher
        self.registers = registers
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            elif processor.registers.current_mode_is_user_or_system():
                print "unpredictable"
            else:
                length = 4 * self.registers.count(1)
                address = processor.registers.get(self.n) if self.increment else sub(
                        processor.registers.get(self.n),
                        BitArray(uint=length, length=32), 32)
                if self.word_higher:
                    address = add(address, BitArray(bin="100"), 32)
                for i in xrange(15):
                    if self.registers[15 - i]:
                        processor.mem_a_set(address, 4, processor.registers.get_rmode(i, BitArray(bin="10000")))
                        address = add(address, BitArray(bin="100"), 32)
                if self.registers[0]:
                    processor.mem_a_set(address, 4, processor.registers.pc_store_value())
