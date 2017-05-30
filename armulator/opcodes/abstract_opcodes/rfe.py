from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add, sub
from bitstring import BitArray
from armulator.arm_exceptions import UndefinedInstructionException
from armulator.enums import InstrSet


class Rfe(AbstractOpcode):
    def __init__(self, increment, word_higher, wback, n):
        super(Rfe, self).__init__()
        self.increment = increment
        self.word_higher = word_higher
        self.wback = wback
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if processor.core_registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            elif (not processor.core_registers.current_mode_is_not_user() or
                  processor.core_registers.current_instr_set() == InstrSet.InstrSet_ThumbEE):
                print "unpredictable"
            else:
                address = processor.core_registers.get(self.n) if self.increment else sub(
                        processor.core_registers.get(self.n),
                        BitArray(bin="1000"), 32)
                if self.word_higher:
                    address = add(address, BitArray(bin="100"), 32)
                new_pc_value = processor.mem_a_get(address, 4)
                spsr_value = processor.mem_a_get(add(address, BitArray(bin="100"), 32), 4)
                if self.wback:
                    processor.core_registers.set(self.n, add(processor.core_registers.get(self.n), BitArray(bin="1000"),
                                                             32) if self.increment else sub(
                            processor.core_registers.get(self.n),
                            BitArray(bin="1000"), 32))
                processor.core_registers.cpsr_write_by_instr(spsr_value, BitArray(bin="1111"), True)
                if (processor.core_registers.cpsr.get_m() == "0b11010" and
                        processor.core_registers.cpsr.get_j() and
                        processor.core_registers.cpsr.get_t()):
                    print "unpredictable"
                else:
                    processor.branch_write_pc(new_pc_value)
