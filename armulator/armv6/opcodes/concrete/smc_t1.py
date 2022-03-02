from armulator.armv6.opcodes.abstract_opcodes.smc import Smc


class SmcT1(Smc):
    @staticmethod
    def from_bitarray(instr, processor):
        if processor.in_it_block() and not processor.last_in_it_block():
            print('unpredictable')
        else:
            return SmcT1(instr)
