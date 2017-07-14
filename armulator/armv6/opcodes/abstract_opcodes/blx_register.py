from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.enums import InstrSet
from bitstring import BitArray


class BlxRegister(AbstractOpcode):
    def __init__(self, m):
        super(BlxRegister, self).__init__()
        self.m = m

    def execute(self, processor):
        if processor.condition_passed():
            target = processor.registers.get(self.m)
            if processor.registers.current_instr_set() == InstrSet.InstrSet_ARM:
                next_instr_addr = BitArray(uint=processor.registers.get_pc().uint - 4, length=32)
                processor.registers.set_lr(next_instr_addr)
            else:
                next_instr_addr = BitArray(uint=processor.registers.get_pc().uint - 2, length=32)
                next_instr_addr[31] = True
                processor.registers.set_lr(next_instr_addr)
            processor.bx_write_pc(target)
