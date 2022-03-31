from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, sign_extend, chain
from armulator.armv6.opcodes.opcode import Opcode


class Ldrsbt(Opcode):
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
                    processor.registers.set(self.t, sign_extend(processor.mem_u_unpriv_get(address, 1), 8, 32))
                    if self.post_index:
                        processor.registers.set(self.n, offset_addr)

    def instruction_syndrome(self):
        if self.t == 15:
            return 0b000000000
        else:
            return chain(0b10010, self.t, 4)
