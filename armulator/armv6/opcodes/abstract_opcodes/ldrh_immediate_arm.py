from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, chain, bit_at
from armulator.armv6.opcodes.opcode import Opcode


class LdrhImmediateArm(Opcode):
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
            data = processor.mem_u_get(address, 2)
            if self.wback:
                processor.registers.set(self.n, offset_addr)
            if processor.unaligned_support() or not bit_at(address, 0):
                processor.registers.set(self.t, data)
            else:
                processor.registers.set(self.t, 0x00000000)  # unknown

    def instruction_syndrome(self):
        if self.t == 15 or self.wback:
            return 0b000000000
        else:
            return chain(0b10100, self.t, 4)
