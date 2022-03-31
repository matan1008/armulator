from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, lower_chunk, chain
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift


class StrRegister(Opcode):
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
                if self.t == 15:
                    data = processor.registers.pc_store_value()
                else:
                    data = processor.registers.get(self.t)
                if (processor.unaligned_support() or lower_chunk(address, 2) == 0b00 or
                        processor.registers.current_instr_set() == InstrSet.ARM):
                    processor.mem_u_set(address, 4, data)
                else:
                    processor.mem_u_set(address, 4, 0x00000000)  # unknown
                if self.wback:
                    processor.registers.set(self.n, offset_addr)

    def instruction_syndrome(self):
        if self.wback:
            return 0b000000000
        else:
            return chain(0b11000, self.t, 4)
