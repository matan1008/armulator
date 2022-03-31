from armulator.armv6.bits_ops import substring, chain
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift


class Pkh(Opcode):
    def __init__(self, instruction, tb_form, m, d, n, shift_t, shift_n):
        super().__init__(instruction)
        self.tb_form = tb_form
        self.m = m
        self.d = d
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            operand2 = shift(processor.registers.get(self.m), 32, self.shift_t, self.shift_n,
                             processor.registers.cpsr.c)
            rd_15 = substring(operand2 if self.tb_form else processor.registers.get(self.n), 15, 0)
            rd_31 = substring(processor.registers.get(self.n) if self.tb_form else operand2, 31, 16)
            processor.registers.set(self.d, chain(rd_31, rd_15, 16))
