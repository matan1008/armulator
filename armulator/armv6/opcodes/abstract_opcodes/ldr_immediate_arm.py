from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, chain, lower_chunk
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import ror


class LdrImmediateArm(Opcode):
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
            data = processor.mem_u_get(address, 4)
            if self.wback:
                processor.registers.set(self.n, offset_addr)
            if self.t == 15:
                if lower_chunk(address, 2) == 0b00:
                    processor.load_write_pc(data)
                else:
                    print('unpredictable')
            elif processor.unaligned_support() or lower_chunk(address, 2) == 0b00:
                processor.registers.set(self.t, data)
            else:
                processor.registers.set(self.t, ror(data, 32, 8 * lower_chunk(address, 2)))

    def instruction_syndrome(self):
        if self.t == 15 or self.wback:
            return 0b000000000
        else:
            return chain(0b11000, self.t, 4)
