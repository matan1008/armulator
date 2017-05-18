from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub


class StrImmediateArm(AbstractOpcode):
    def __init__(self, add, wback, index, t, n, imm32):
        super(StrImmediateArm, self).__init__()
        self.add = add
        self.wback = wback
        self.index = index
        self.t = t
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            offset_addr = bits_add(processor.core_registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                    processor.core_registers.get(self.n), self.imm32, 32)
            address = offset_addr if self.index else processor.core_registers.get(self.n)
            processor.mem_u_set(
                    address,
                    4,
                    processor.core_registers.pc_store_value() if self.t == 15 else processor.core_registers.get(self.t)
            )
            if self.wback:
                processor.core_registers.set(self.n, offset_addr)
