from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class CpsArm(AbstractOpcode):
    def __init__(self, affect_a, affect_i, affect_f, enable, disable, change_mode, mode):
        super(CpsArm, self).__init__()
        self.affect_a = affect_a
        self.affect_i = affect_i
        self.affect_f = affect_f
        self.enable = enable
        self.disable = disable
        self.change_mode = change_mode
        self.mode = mode

    def execute(self, processor):
        if processor.core_registers.current_mode_is_not_user():
            cpsr_val = processor.core_registers.cpsr.value
            if self.enable:
                if self.affect_a:
                    cpsr_val[23] = False
                if self.affect_i:
                    cpsr_val[24] = False
                if self.affect_f:
                    cpsr_val[25] = False
            if self.disable:
                if self.affect_a:
                    cpsr_val[23] = True
                if self.affect_i:
                    cpsr_val[24] = True
                if self.affect_f:
                    cpsr_val[25] = True
            if self.change_mode:
                cpsr_val[27:32] = self.mode
            processor.core_registers.cpsr_write_by_instr(cpsr_val, BitArray(bin="1111"), False)
