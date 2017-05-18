from armulator.opcodes.abstract_opcode import AbstractOpcode


class It(AbstractOpcode):
    def __init__(self, firstcond, mask):
        super(It, self).__init__()
        self.firstcond = firstcond
        self.mask = mask

    def execute(self, processor):
        processor.core_registers.set_cpsr_itstate(self.firstcond + self.mask)
