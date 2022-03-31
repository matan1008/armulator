from armulator.armv6.bits_ops import sub, lowest_set_bit_ref, bit_at, bit_count
from armulator.armv6.opcodes.opcode import Opcode


class Stmda(Opcode):
    def __init__(self, instruction, wback, registers, n):
        super().__init__(instruction)
        self.wback = wback
        self.registers = registers
        self.n = n

    def execute(self, processor):
        register_count = bit_count(self.registers, 1, 16)
        if processor.condition_passed():
            address = sub(processor.registers.get(self.n), (4 * register_count), 32) + 4
            for i in range(15):
                if bit_at(self.registers, i):
                    if i == self.n and self.wback and i != lowest_set_bit_ref(self.registers):
                        processor.mem_a_set(address, 4, 0x00000000)  # unknown
                    else:
                        processor.mem_a_set(address, 4, processor.registers.get(i))
                    address = address + 4
            if bit_at(self.registers, 15):
                processor.mem_a_set(address, 4, processor.registers.pc_store_value())
            if self.wback:
                processor.registers.set(self.n, sub(processor.registers.get(self.n), 4 * register_count, 32))
