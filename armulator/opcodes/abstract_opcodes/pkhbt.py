from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift


class Pkhbt(AbstractOpcode):
    def __init__(self, tb_form, m, d, n, shift_t, shift_n):
        super(Pkhbt, self).__init__()
        self.tb_form = tb_form
        self.m = m
        self.d = d
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            operand2 = shift(processor.core_registers.get(self.m), self.shift_t, self.shift_n,
                             processor.core_registers.get_cpsr_c())
            temp_rd = processor.core_registers.get(self.n)[0:16] if self.tb_form else operand2[0:16]
            temp_rd += operand2[16:32] if self.tb_form else processor.core_registers.get(self.n)[16:32]
            processor.core_registers.set(self.d, temp_rd)
