from armulator.armv6.bits_ops import lower_chunk
from armulator.armv6.opcodes.opcode import Opcode


class Svc(Opcode):
    def __init__(self, instruction, imm32):
        super().__init__(instruction)
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            processor.call_supervisor(lower_chunk(self.imm32, 16))
