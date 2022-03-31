from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, lower_chunk, chain
from armulator.armv6.configurations import have_lpae
from armulator.armv6.opcodes.opcode import Opcode


class StrdImmediate(Opcode):
    def __init__(self, instruction, add, wback, index, imm32, t, t2, n):
        super().__init__(instruction)
        self.add = add
        self.wback = wback
        self.index = index
        self.imm32 = imm32
        self.t = t
        self.t2 = t2
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                offset_addr = bits_add(processor.registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                    processor.registers.get(self.n), self.imm32, 32)
                address = offset_addr if self.index else processor.registers.get(self.n)
                if have_lpae() and lower_chunk(address, 3) == 0b000:
                    if processor.big_endian():
                        data = chain(processor.registers.get(self.t), processor.registers.get(self.t2), 32)
                    else:
                        data = chain(processor.registers.get(self.t2), processor.registers.get(self.t), 32)
                    processor.mem_a_set(address, 8, data)
                else:
                    processor.mem_a_set(address, 4, processor.registers.get(self.t))
                    processor.mem_a_set(bits_add(address, 4, 32), 4, processor.registers.get(self.t2))
                if self.wback:
                    processor.registers.set(self.n, offset_addr)
