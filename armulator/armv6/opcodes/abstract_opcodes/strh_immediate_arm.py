from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, chain, bit_at, substring
from armulator.armv6.opcodes.opcode import Opcode


class StrhImmediateArm(Opcode):
    def __init__(self, instruction, add, wback, index, imm32, t, n):
        super().__init__(instruction)
        self.add = add
        self.wback = wback
        self.index = index
        self.imm32 = imm32
        self.t = t
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            offset_addr = bits_add(processor.registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                processor.registers.get(self.n), self.imm32, 32)
            address = offset_addr if self.index else processor.registers.get(self.n)
            if processor.unaligned_support() or not bit_at(address, 0):
                processor.mem_u_set(address, 2, substring(processor.registers.get(self.t), 15, 0))
            else:
                processor.mem_u_set(address, 2, 0x0000)  # unknown
            if self.wback:
                processor.registers.set(self.n, offset_addr)

    def instruction_syndrome(self):
        if self.wback:
            return 0b000000000
        else:
            return chain(0b10100, self.t, 4)
