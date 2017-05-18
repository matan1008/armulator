from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction
from armulator.configurations import HaveLPAE


class LdrdImmediate(AbstractOpcode):
    def __init__(self, add, wback, index, imm32, t, t2, n):
        super(LdrdImmediate, self).__init__()
        self.add = add
        self.wback = wback
        self.index = index
        self.imm32 = imm32
        self.t = t
        self.t2 = t2
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                offset_addr = bits_add(processor.core_registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                        processor.core_registers.get(self.n), self.imm32, 32)
                address = offset_addr if self.index else processor.core_registers.get(self.n)
                if HaveLPAE() and address[29:32] == "0b000":
                    data = processor.mem_a_get(address, 8)
                    if processor.big_endian():
                        processor.core_registers.set(self.t, data[0:32])
                        processor.core_registers.set(self.t2, data[32:64])
                    else:
                        processor.core_registers.set(self.t, data[32:64])
                        processor.core_registers.set(self.t2, data[0:32])
                else:
                    processor.core_registers.set(self.t, processor.mem_a_get(address, 4))
                    processor.core_registers.set(self.t2,
                                                 processor.mem_a_get(bits_add(address, BitArray(bin="0b000"), 32), 4))
                if self.wback:
                    processor.core_registers.set(self.n, offset_addr)
