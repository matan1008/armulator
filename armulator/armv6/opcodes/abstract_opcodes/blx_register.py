from armulator.armv6.bits_ops import set_bit_at
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.opcode import Opcode


class BlxRegister(Opcode):
    def __init__(self, instruction, m):
        super().__init__(instruction)
        self.m = m

    def execute(self, processor):
        if processor.condition_passed():
            target = processor.registers.get(self.m)
            if processor.registers.current_instr_set() == InstrSet.ARM:
                next_instr_addr = processor.registers.get_pc() - 4
                processor.registers.set_lr(next_instr_addr)
            else:
                next_instr_addr = processor.registers.get_pc() - 2
                next_instr_addr = set_bit_at(next_instr_addr, 0, 1)
                processor.registers.set_lr(next_instr_addr)
            processor.bx_write_pc(target)
