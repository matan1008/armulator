from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add, lowest_set_bit_ref
from bitstring import BitArray


class Stmib(AbstractOpcode):
    def __init__(self, wback, registers, n):
        super(Stmib, self).__init__()
        self.wback = wback
        self.registers = registers
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            address = add(processor.registers.get(self.n), BitArray(bin="100"), 32)
            for i in xrange(15):
                if self.registers[15 - i]:
                    if i == self.n and self.wback and i != lowest_set_bit_ref(self.registers):
                        processor.mem_a_set(address, 4, BitArray(length=32))  # unknown
                    else:
                        processor.mem_a_set(address, 4, processor.registers.get(i))
                    address = add(address, BitArray(bin="100"), 32)
            if self.registers[0]:
                processor.mem_a_set(address, 4, processor.registers.pc_store_value())
            if self.wback:
                processor.registers.set(
                    self.n,
                    add(processor.registers.get(self.n), BitArray(uint=(4 * self.registers.count(1)), length=32), 32)
                )
