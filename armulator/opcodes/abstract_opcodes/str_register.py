from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction
from armulator.shift import shift
from armulator.enums import InstrSet


class StrRegister(AbstractOpcode):
    def __init__(self, add, wback, index, m, t, n, shift_t, shift_n):
        super(StrRegister, self).__init__()
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
                offset = shift(processor.core_registers.get(self.m), self.shift_t, self.shift_n,
                               processor.core_registers.cpsr.get_c())
                offset_addr = bits_add(processor.core_registers.get(self.n), offset, 32) if self.add else bits_sub(
                        processor.core_registers.get(self.n), offset, 32)
                address = offset_addr if self.index else processor.core_registers.get(self.n)
                if self.t == 15:
                    data = processor.core_registers.pc_store_value()
                else:
                    data = processor.core_registers.get(self.t)
                if (processor.unaligned_support() or
                        address[30:32] == "0b00" or
                        processor.core_registers.current_instr_set() == InstrSet.InstrSet_ARM):
                    processor.mem_u_set(address, 4, data)
                else:
                    processor.mem_u_set(address, 4, BitArray(length=32))  # unknown
                if self.wback:
                    processor.core_registers.set(self.n, offset_addr)
