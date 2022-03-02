from armulator.armv6.configurations import have_virt_ext, jazelle_accepts_execution
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.opcode import Opcode


class Bxj(Opcode):
    def __init__(self, instruction, m):
        super().__init__(instruction)
        self.m = m

    def execute(self, processor):
        if processor.condition_passed():
            if (have_virt_ext() and not processor.registers.is_secure() and
                    not processor.registers.current_mode_is_hyp() and
                    processor.registers.hstr.tjdbx):
                hsr_string = self.m
                processor.write_hsr(0b001010, hsr_string)
                processor.registers.take_hyp_trap_exception()
            elif (not processor.registers.jmcr.je or
                  processor.registers.current_instr_set() == InstrSet.THUMB_EE):
                processor.bx_write_pc(processor.registers.get(self.m))
            else:
                if jazelle_accepts_execution():
                    processor.switch_to_jazelle_execution()
                else:
                    # SUBARCHITECTURE_DEFINED handler call
                    raise NotImplementedError()
