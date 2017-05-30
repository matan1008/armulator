from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub, sign_extend
from armulator.arm_exceptions import EndOfInstruction


class LdrsbImmediate(AbstractOpcode):
    def __init__(self, add, wback, index, imm32, t, n):
        super(LdrsbImmediate, self).__init__()
        self.add = add
        self.wback = wback
        self.index = index
        self.imm32 = imm32
        self.t = t
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(15)
            except EndOfInstruction:
                pass
            else:
                offset_addr = bits_add(processor.registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                        processor.registers.get(self.n), self.imm32, 32)
                address = offset_addr if self.index else processor.registers.get(self.n)
                processor.registers.set(self.t, sign_extend(processor.mem_u_get(address, 1), 32))
                if self.wback:
                    processor.registers.set(self.n, offset_addr)
