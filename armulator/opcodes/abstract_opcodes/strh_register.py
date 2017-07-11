from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction
from armulator.shift import shift


class StrhRegister(AbstractOpcode):
    def __init__(self, add, wback, index, m, t, n, shift_t, shift_n):
        super(StrhRegister, self).__init__()
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
                offset = shift(processor.registers.get(self.m), self.shift_t, self.shift_n,
                               processor.registers.cpsr.get_c())
                offset_addr = bits_add(processor.registers.get(self.n), offset, 32) if self.add else bits_sub(
                    processor.registers.get(self.n), offset, 32)
                address = offset_addr if self.index else processor.registers.get(self.n)
                if processor.unaligned_support() or not address[31]:
                    processor.mem_u_set(address, 2, processor.registers.get(self.t)[16:32])
                else:
                    processor.mem_u_set(address, 2, BitArray(length=16))  # unknown
                if self.wback:
                    processor.registers.set(self.n, offset_addr)

    def instruction_syndrome(self):
        if self.wback:
            return BitArray(length=9)
        else:
            return BitArray(bin="10100") + BitArray(uint=self.t, length=4)
