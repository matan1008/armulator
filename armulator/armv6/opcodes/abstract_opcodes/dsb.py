from armulator.armv6.configurations import have_virt_ext
from armulator.armv6.enums import MBReqDomain, MBReqTypes
from armulator.armv6.opcodes.opcode import Opcode


class Dsb(Opcode):
    def __init__(self, instruction, option):
        super().__init__(instruction)
        self.option = option

    def execute(self, processor):
        if processor.condition_passed():
            if self.option == 0b0010:
                domain = MBReqDomain.OUTER_SHAREABLE
                types = MBReqTypes.WRITES
            elif self.option == 0b0011:
                domain = MBReqDomain.OUTER_SHAREABLE
                types = MBReqTypes.ALL
            elif self.option == 0b0110:
                domain = MBReqDomain.NONSHAREABLE
                types = MBReqTypes.WRITES
            elif self.option == 0b0111:
                domain = MBReqDomain.NONSHAREABLE
                types = MBReqTypes.ALL
            elif self.option == 0b1010:
                domain = MBReqDomain.INNER_SHAREABLE
                types = MBReqTypes.WRITES
            elif self.option == 0b1011:
                domain = MBReqDomain.INNER_SHAREABLE
                types = MBReqTypes.ALL
            elif self.option == 0b1110:
                domain = MBReqDomain.FULL_SYSTEM
                types = MBReqTypes.WRITES
            else:
                domain = MBReqDomain.FULL_SYSTEM
                types = MBReqTypes.ALL
            if (have_virt_ext() and
                    not processor.registers.is_secure() and
                    not processor.registers.current_mode_is_hyp()):
                if processor.registers.hcr.bsu == 0b11:
                    domain = MBReqDomain.FULL_SYSTEM
                if processor.registers.hcr.bsu == 0b10 and domain != MBReqDomain.FULL_SYSTEM:
                    domain = MBReqDomain.OUTER_SHAREABLE
                if processor.registers.hcr.bsu == 0b01 and domain == MBReqDomain.NONSHAREABLE:
                    domain = MBReqDomain.INNER_SHAREABLE
            processor.data_synchronization_barrier(domain, types)
