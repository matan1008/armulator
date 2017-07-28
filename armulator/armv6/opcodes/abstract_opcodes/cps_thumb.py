from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class CpsThumb(AbstractOpcode):
    def __init__(self, affect_a, affect_i, affect_f, enable, disable, change_mode, mode="0b00000"):
        super(CpsThumb, self).__init__()
        self.affect_a = affect_a
        self.affect_i = affect_i
        self.affect_f = affect_f
        self.enable = enable
        self.disable = disable
        self.change_mode = change_mode
        self.mode = mode

    def execute(self, processor):
        if processor.registers.current_mode_is_not_user():
            cpsr_val = processor.registers.cpsr.value.copy()
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
            processor.registers.cpsr_write_by_instr(cpsr_val, BitArray(bin="1111"), False)
            if (processor.registers.cpsr.get_m() == "0b11010" and
                    processor.registers.cpsr.get_j() and
                    processor.registers.cpsr.get_t()):
                print "unpredictable"
