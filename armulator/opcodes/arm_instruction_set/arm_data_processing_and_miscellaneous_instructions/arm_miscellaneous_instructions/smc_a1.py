from armulator.opcodes.abstract_opcodes.smc import Smc
from armulator.opcodes.opcode import Opcode
from bitstring import BitArray


class SmcA1(Smc, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Smc.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = BitArray(bin=("0" * 28 + instr.bin[-4:]))
        return SmcA1(instr)
