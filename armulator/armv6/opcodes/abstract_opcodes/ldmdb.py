from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add, sub, bit_count, bit_at
from armulator.armv6.opcodes.opcode import Opcode


class Ldmdb(Opcode):
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
                address = sub(processor.registers.get(self.n), 4 * bit_count(self.registers, 1, 16), 32)
                for i in range(15):
                    if bit_at(self.registers, i):
                        processor.registers.set(i, processor.mem_a_get(address, 4))
                        address = add(address, 4, 32)
                if bit_at(self.registers, 15):
                    processor.load_write_pc(processor.mem_a_get(address, 4))
                if self.wback and not bit_at(self.registers, self.n):
                    processor.registers.set(
                        self.n, sub(processor.registers.get(self.n), 4 * bit_count(self.registers, 1, 16), 32)
                    )
                if self.wback and bit_at(self.registers, self.n):
                    processor.registers.set(self.n, 0x00000000)  # unknown
