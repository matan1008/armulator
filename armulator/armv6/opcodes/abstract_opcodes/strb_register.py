from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, chain, lower_chunk
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift


class StrbRegister(Opcode):
    def __init__(self, instruction, add, wback, index, m, t, n, shift_t, shift_n):
        super().__init__(instruction)
        self.add = add
        self.wback = wback
        self.index = index
        self.m = m
        self.t = t
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                offset = shift(processor.registers.get(self.m), 32, self.shift_t, self.shift_n,
                               processor.registers.cpsr.c)
                offset_addr = bits_add(processor.registers.get(self.n), offset, 32) if self.add else bits_sub(
                    processor.registers.get(self.n), offset, 32)
                address = offset_addr if self.index else processor.registers.get(self.n)
                processor.mem_u_set(address, 1, lower_chunk(processor.registers.get(self.t), 8))
                if self.wback:
                    processor.registers.set(self.n, offset_addr)

    def instruction_syndrome(self):
        if self.wback:
            return 0b000000000
        else:
            return chain(0b10000, self.t, 4)
