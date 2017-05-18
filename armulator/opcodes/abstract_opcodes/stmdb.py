from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add, sub, lowest_set_bit_ref
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction


class Stmdb(AbstractOpcode):
    def __init__(self, wback, registers, n):
        super(Stmdb, self).__init__()
        self.wback = wback
        self.registers = registers
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                address = sub(processor.core_registers.get(self.n),
                              BitArray(uint=(4 * self.registers.count(1)), length=32),
                              32)
                for i in xrange(15):
                    if self.registers[15 - i]:
                        if i == self.n and self.wback and i != lowest_set_bit_ref(self.registers):
                            processor.mem_a_set(address, 4, BitArray(length=32))  # unknown
                        else:
                            processor.mem_a_set(address, 4, processor.core_registers.get(i))
                        address = add(address, BitArray(bin="100"), 32)
                if self.registers[0]:
                    processor.mem_a_set(address, 4, processor.core_registers.pc_store_value())
                if self.wback:
                    processor.core_registers.set(self.n, sub(processor.core_registers.get(self.n),
                                                             BitArray(uint=(4 * self.registers.count(1)), length=32),
                                                             32))
