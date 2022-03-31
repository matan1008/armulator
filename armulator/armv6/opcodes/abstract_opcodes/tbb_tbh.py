from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import lsl


class TbbTbh(Opcode):
    def __init__(self, instruction, is_tbh, m, n):
        super().__init__(instruction)
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
                        add(processor.registers.get(self.n), lsl(processor.registers.get(self.m), 32, 1), 32), 2)
                else:
                    halfwords = processor.mem_u_get(
                        add(processor.registers.get(self.n), processor.registers.get(self.m), 32), 1)
                processor.branch_write_pc(add(processor.registers.get_pc(), 2 * halfwords, 32))
