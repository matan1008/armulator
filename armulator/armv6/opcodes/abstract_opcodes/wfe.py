from armulator.armv6.configurations import have_virt_ext
from armulator.armv6.opcodes.opcode import Opcode


class Wfe(Opcode):
    def execute(self, processor):
        if processor.condition_passed():
            if processor.event_registered():
                processor.clear_event_register()
            else:
                if (have_virt_ext() and not processor.registers.is_secure() and
                        not processor.registers.current_mode_is_hyp() and
                        processor.registers.hcr.twe):
                    hsr_string = 0b0000000000000000000000001
                    processor.write_hsr(0b000001, hsr_string)
                    processor.registers.take_hyp_trap_exception()
                else:
                    processor.wait_for_event()
