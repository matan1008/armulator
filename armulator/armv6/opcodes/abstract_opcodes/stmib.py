from armulator.armv6.bits_ops import add, lowest_set_bit_ref, bit_at, bit_count
from armulator.armv6.opcodes.opcode import Opcode


class Stmib(Opcode):
    def __init__(self, instruction, wback, registers, n):
        super().__init__(instruction)
        self.wback = wback
        self.registers = registers
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            address = add(processor.registers.get(self.n), 4, 32)
            for i in range(15):
                if bit_at(self.registers, i):
                    if i == self.n and self.wback and i != lowest_set_bit_ref(self.registers):
                        processor.mem_a_set(address, 4, 0x00000000)  # unknown
                    else:
                        processor.mem_a_set(address, 4, processor.registers.get(i))
                    address = add(address, 4, 32)
            if bit_at(self.registers, 15):
                processor.mem_a_set(address, 4, processor.registers.pc_store_value())
            if self.wback:
                processor.registers.set(
                    self.n, add(processor.registers.get(self.n), 4 * bit_count(self.registers, 1, 16), 32)
                )
