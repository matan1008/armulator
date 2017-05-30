from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction


class StrhImmediateThumb(AbstractOpcode):
    def __init__(self, add, wback, index, t, n, imm32):
        super(StrhImmediateThumb, self).__init__()
        self.add = add
        self.wback = wback
        self.index = index
        self.t = t
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                offset_addr = bits_add(processor.registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                        processor.registers.get(self.n), self.imm32, 32)
                address = offset_addr if self.index else processor.registers.get(self.n)
                if processor.unaligned_support() or address[31:32] == "0b0":
                    processor.mem_u_set(address, 2, processor.registers.get(self.t)[16:32])
                else:
                    processor.mem_u_set(address, 2, BitArray(length=16))  # unknown
                if self.wback:
                    processor.registers.set(self.n, offset_addr)
