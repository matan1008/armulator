from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add, chain, lower_chunk
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift


class LdrRegisterThumb(Opcode):
    def __init__(self, instruction, m, t, n, shift_t, shift_n):
        super().__init__(instruction)
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
                address = add(processor.registers.get(self.n), offset, 32)
                data = processor.mem_u_get(address, 4)
                if self.t == 15:
                    if lower_chunk(address, 2) == 0b00:
                        processor.load_write_pc(address)
                    else:
                        print('unpredictable')
                elif processor.unaligned_support() or lower_chunk(address, 2) == 0b00:
                    processor.registers.set(self.t, data)
                else:
                    processor.registers.set(self.t, 0x00000000)  # unknown

    def instruction_syndrome(self):
        if self.t == 15:
            return 0b000000000
        else:
            return chain(0b11000, self.t, 4)
