from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub


class PldImmediate(AbstractOpcode):
    def __init__(self, add, is_pldw, n, imm32):
        super(PldImmediate, self).__init__()
        self.add = add
        self.is_pldw = is_pldw
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            address = bits_add(processor.registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                    processor.registers.get(self.n), self.imm32, 32)
            if self.is_pldw:
                processor.hint_preload_data_for_write(address)
            else:
                processor.hint_preload_data(address)
