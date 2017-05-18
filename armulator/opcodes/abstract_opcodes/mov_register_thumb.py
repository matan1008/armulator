from armulator.opcodes.abstract_opcode import AbstractOpcode


class MovRegisterThumb(AbstractOpcode):
    def __init__(self, setflags, m, d):
        super(MovRegisterThumb, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.core_registers.get(self.m)
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.core_registers.set(self.d, result)
                if self.setflags:
                    processor.core_registers.set_cpsr_n(result[0])
                    processor.core_registers.set_cpsr_z(result.all(0))
