from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, lower_chunk, chain
from armulator.armv6.opcodes.opcode import Opcode


class StrbImmediateArm(Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        super().__init__(instruction)
        self.add = add
        self.wback = wback
        self.index = index
        self.t = t
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            offset_addr = bits_add(processor.registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                processor.registers.get(self.n), self.imm32, 32)
            address = offset_addr if self.index else processor.registers.get(self.n)
            processor.mem_u_set(address, 1, lower_chunk(processor.registers.get(self.t), 8))
            if self.wback:
                processor.registers.set(self.n, offset_addr)

    def instruction_syndrome(self):
        if self.wback:
            return 0b000000000
        else:
            return chain(0b10000, self.t, 4)
