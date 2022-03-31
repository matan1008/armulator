from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, chain, substring
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift, SRType


class Strt(Opcode):
    def __init__(self, instruction, add, register_form, post_index, t, n, m=0, shift_t=SRType.LSL, shift_n=0, imm32=0):
        super().__init__(instruction)
        self.add = add
        self.register_form = register_form
        self.post_index = post_index
        self.t = t
        self.n = n
        self.m = m
        self.shift_t = shift_t
        self.shift_n = shift_n
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
                    offset = shift(processor.registers.get(self.m), 32, self.shift_t, self.shift_n,
                                   processor.registers.cpsr.c) if self.register_form else self.imm32
                    offset_addr = bits_add(processor.registers.get(self.n), offset, 32) if self.add else bits_sub(
                        processor.registers.get(self.n), offset, 32)
                    address = processor.registers.get(self.n) if self.post_index else offset_addr
                    if self.t == 15:
                        data = processor.registers.pc_store_value()
                    else:
                        data = processor.registers.get(self.t)
                    if (processor.unaligned_support() or
                            substring(address, 1, 0) == 0b00 or
                            processor.registers.current_instr_set() == InstrSet.ARM):
                        processor.mem_u_unpriv_set(address, 4, data)
                    else:
                        processor.mem_u_unpriv_set(address, 4, 0x00000000)  # unknown
                    if self.post_index:
                        processor.registers.set(self.n, offset_addr)

    def instruction_syndrome(self):
        return chain(0b11000, self.t, 4)
