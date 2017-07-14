from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.shift import shift
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub


class PldRegister(AbstractOpcode):
    def __init__(self, add, is_pldw, m, n, shift_t, shift_n):
        super(PldRegister, self).__init__()
        self.add = add
        self.is_pldw = is_pldw
        self.m = m
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            offset = shift(processor.registers.get(self.m), self.shift_t, self.shift_n,
                           processor.registers.cpsr.get_c())
            address = bits_add(processor.registers.get(self.n), offset, 32) if self.add else bits_sub(
                    processor.registers.get(self.n), offset, 32)
            if self.is_pldw:
                processor.hint_preload_data_for_write(address)
            else:
                processor.hint_preload_data(address)
