from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.configurations import HaveVirtExt


class Wfe(AbstractOpcode):
    def __init__(self):
        super(Wfe, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            if processor.event_registered():
                processor.clear_event_register()
            else:
                if (HaveVirtExt() and not processor.registers.is_secure() and
                        not processor.registers.current_mode_is_hyp() and
                        processor.registers.hcr.get_twe()):
                    hsr_string = BitArray(length=25)
                    hsr_string[24] = True
                    processor.write_hsr(BitArray(bin="000001"), hsr_string)
                    processor.registers.take_hyp_trap_exception()
                else:
                    processor.wait_for_event()
