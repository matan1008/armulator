from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub
from bitstring import BitArray


class StrhImmediateArm(AbstractOpcode):
    def __init__(self, add, wback, index, imm32, t, n):
        super(StrhImmediateArm, self).__init__()
        self.add = add
        self.wback = wback
        self.index = index
        self.imm32 = imm32
        self.t = t
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            offset_addr = bits_add(processor.core_registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                    processor.core_registers.get(self.n), self.imm32, 32)
            address = offset_addr if self.index else processor.core_registers.get(self.n)
            if processor.unaligned_support() or not address[31]:
                processor.mem_u_set(address, 2, processor.core_registers.get(self.t)[16:32])
            else:
                processor.mem_u_set(address, 2, BitArray(length=16))  # unknown
            if self.wback:
                processor.core_registers.set(self.n, offset_addr)
