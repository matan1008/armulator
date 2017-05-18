from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.arm_exceptions import EndOfInstruction
from armulator.bits_ops import add
from armulator.shift import lsl
from bitstring import BitArray


class Tbb(AbstractOpcode):
    def __init__(self, is_tbh, m, n):
        super(Tbb, self).__init__()
        self.is_tbh = is_tbh
        self.m = m
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                if self.is_tbh:
                    halfwords = processor.mem_u_get(
                            add(processor.core_registers.get(self.n), lsl(processor.core_registers.get(self.m), 1), 32),
                            2).uint
                else:
                    halfwords = processor.mem_u_get(
                        add(processor.core_registers.get(self.n), processor.core_registers.get(self.m), 32), 1).uint
                processor.branch_write_pc(add(processor.core_registers.get_pc(), BitArray(uint=2 * halfwords), 32))
