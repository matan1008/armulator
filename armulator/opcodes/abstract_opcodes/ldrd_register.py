from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub
from bitstring import BitArray
from armulator.configurations import HaveLPAE


class LdrdRegister(AbstractOpcode):
    def __init__(self, add, wback, index, m, t, t2, n):
        super(LdrdRegister, self).__init__()
        self.add = add
        self.wback = wback
        self.index = index
        self.m = m
        self.t = t
        self.t2 = t2
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            offset_addr = bits_add(processor.core_registers.get(self.n), processor.core_registers.get(self.m),
                                   32) if self.add else bits_sub(processor.core_registers.get(self.n),
                                                                 processor.core_registers.get(self.m), 32)
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
                                             processor.mem_a_get(bits_add(address, BitArray(bin="100"), 32), 4))
            if self.wback:
                processor.core_registers.set(self.n, offset_addr)
