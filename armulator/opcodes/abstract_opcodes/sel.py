from armulator.opcodes.abstract_opcode import AbstractOpcode


class Sel(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Sel, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            ge = processor.core_registers.get_cpsr_ge()
            temp_rd = processor.core_registers.get(self.n)[0:8] if ge[0] == "1" else processor.core_registers.get(
                    self.m)[0:8]
            temp_rd += processor.core_registers.get(self.n)[8:16] if ge[1] == "1" else processor.core_registers.get(
                    self.m)[8:16]
            temp_rd += processor.core_registers.get(self.n)[16:24] if ge[2] == "1" else processor.core_registers.get(
                    self.m)[16:24]
            temp_rd += processor.core_registers.get(self.n)[24:32] if ge[3] == "1" else processor.core_registers.get(
                    self.m)[24:32]
            processor.core_registers.set(self.d, temp_rd)
