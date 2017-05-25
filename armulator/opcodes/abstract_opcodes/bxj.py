from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.bits_ops import zeros
from armulator.configurations import HaveVirtExt, JazelleAcceptsExecution
from armulator.enums import InstrSet


class Bxj(AbstractOpcode):
    def __init__(self, m):
        super(Bxj, self).__init__()
        self.m = m

    def execute(self, processor):
        if processor.condition_passed():
            if (HaveVirtExt() and not processor.core_registers.is_secure() and
                    not processor.core_registers.current_mode_is_hyp() and
                    processor.core_registers.hstr.get_tjdbx()):
                hsr_string = zeros(25)
                hsr_string[-4:] = self.m
                processor.write_hsr(BitArray(bin="001010"), hsr_string)
                processor.core_registers.take_hyp_trap_exception()
            elif (not processor.core_registers.jmcr.get_je() or
                  processor.core_registers.current_instr_set() == InstrSet.InstrSet_ThumbEE):
                processor.bx_write_pc(processor.core_registers.get(self.m))
            else:
                if JazelleAcceptsExecution():
                    processor.switch_to_jazelle_execution()
                else:
                    # SUBARCHITECTURE_DEFINED handler call
                    raise NotImplementedError()
