from armulator.armv6.bits_ops import substring, chain
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import ror, shift


class LdrRegisterArm(Opcode):
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
            offset = shift(processor.registers.get(self.m), 32, self.shift_t, self.shift_n, processor.registers.cpsr.c)
            n = processor.registers.get(self.n)
            offset_addr = (n + offset) if self.add else (n - offset)
            address = offset_addr if self.index else n
            data = processor.mem_u_get(address, 4)
            if self.wback:
                processor.registers.set(self.n, offset_addr)
            if self.t == 15:
                if substring(address, 1, 0) == 0b00:
                    processor.load_write_pc(address)
                else:
                    print('unpredictable')
            elif processor.unaligned_support() or substring(address, 1, 0) == 0b00:
                processor.registers.set(self.t, data)
            else:
                processor.registers.set(self.t, ror(data, 32, 8 * substring(address, 1, 0)))

    def instruction_syndrome(self):
        if self.t == 15 or self.wback:
            return 0b000000000
        else:
            return chain(0b11000, self.t, 4)
