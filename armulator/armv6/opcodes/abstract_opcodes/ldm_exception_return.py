from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add, sub
from bitstring import BitArray
from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.enums import InstrSet


class LdmExceptionReturn(AbstractOpcode):
    def __init__(self, increment, word_higher, wback, registers, n):
        super(LdmExceptionReturn, self).__init__()
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
                  processor.registers.current_instr_set() == InstrSet.InstrSet_ThumbEE):
                print "unpredictable"
            else:
                length = 4 * self.registers.count(1) + 4
                address = processor.registers.get(self.n) if self.increment else sub(
                        processor.registers.get(self.n),
                        BitArray(uint=length, length=32), 32)
                if self.word_higher:
                    address = add(address, BitArray(bin="100"), 32)
                for i in xrange(15):
                    if self.registers[15 - i]:
                        processor.registers.set(i, processor.mem_a_get(address, 4))
                        address = add(address, BitArray(bin="100"), 32)
                new_pc_value = processor.mem_a_get(address, 4)
                if self.wback and not self.registers[15 - self.n]:
                    processor.registers.set(
                        self.n,
                        (add(processor.registers.get(self.n), BitArray(uint=length, length=32), 32)
                         if self.increment
                         else sub(processor.registers.get(self.n), BitArray(uint=length, length=32), 32))
                    )
                if self.wback and self.registers[15 - self.n]:
                    processor.registers.set(self.n, BitArray(length=32))  # unknown
                processor.registers.cpsr_write_by_instr(processor.registers.get_spsr(), BitArray(bin="1111"), True)
                if (processor.registers.cpsr.get_m() == "0b11010" and
                        processor.registers.cpsr.get_j() and
                        processor.registers.cpsr.get_t()):
                    print "unpredictable"
                else:
                    processor.branch_write_pc(new_pc_value)
