from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add, lowest_set_bit_ref, bit_at
from armulator.armv6.opcodes.opcode import Opcode


class Stm(Opcode):
    def __init__(self, instruction, wback, registers, n):
        super().__init__(instruction)
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
                address = processor.registers.get(self.n)
                write_count = 0
                for i in range(15):
                    if bit_at(self.registers, i):
                        if i == self.n and self.wback and i != lowest_set_bit_ref(self.registers):
                            processor.mem_a_set(address, 4, 0x00000000)  # unknown
                        else:
                            processor.mem_a_set(address, 4, processor.registers.get(i))
                        address = add(address, 0b100, 32)
                        write_count += 1
                if bit_at(self.registers, 15):
                    processor.mem_a_set(address, 4, processor.registers.pc_store_value())
                if self.wback:
                    processor.registers.set(self.n, add(processor.registers.get(self.n), 4 * write_count, 32))
