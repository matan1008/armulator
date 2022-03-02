from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, chain, lower_chunk, bit_at
from armulator.armv6.opcodes.opcode import Opcode


class Strht(Opcode):
    def __init__(self, instruction, add, register_form, post_index, t, n, m=0, imm32=0):
        super().__init__(instruction)
        self.add = add
        self.register_form = register_form
        self.post_index = post_index
        self.t = t
        self.n = n
        self.m = m
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_mode_is_hyp():
                print('unpredictable')
            else:
                try:
                    processor.null_check_if_thumbee(self.n)
                except EndOfInstruction:
                    pass
                else:
                    offset = processor.registers.get(self.m) if self.register_form else self.imm32
                    offset_addr = bits_add(processor.registers.get(self.n), offset, 32) if self.add else bits_sub(
                        processor.registers.get(self.n), offset, 32)
                    address = processor.registers.get(self.n) if self.post_index else offset_addr
                    if processor.unaligned_support() or not bit_at(address, 0):
                        processor.mem_u_unpriv_set(address, 2, lower_chunk(processor.registers.get(self.t), 16))
                    else:
                        processor.mem_u_unpriv_set(address, 2, 0x0000)  # unknown
                    if self.post_index:
                        processor.registers.set(self.n, offset_addr)

    def instruction_syndrome(self):
        return chain(0b10100, self.t, 4)
