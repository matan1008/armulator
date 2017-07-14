from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.armv6.configurations import have_virt_ext


class Wfi(AbstractOpcode):
    def __init__(self):
        super(Wfi, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            if (have_virt_ext() and not processor.registers.is_secure() and
                    not processor.registers.current_mode_is_hyp() and
                    processor.registers.hcr.get_twi()):
                hsr_string = BitArray(length=25)
                processor.write_hsr(BitArray(bin="000001"), hsr_string)
                processor.registers.take_hyp_trap_exception()
            else:
                processor.wait_for_interrupt()
