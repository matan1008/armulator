from armulator.armv6.opcodes.abstract_opcodes.bkpt import Bkpt


class BkptT1(Bkpt):
    @staticmethod
    def from_bitarray(instr, processor):
        return BkptT1(instr)
