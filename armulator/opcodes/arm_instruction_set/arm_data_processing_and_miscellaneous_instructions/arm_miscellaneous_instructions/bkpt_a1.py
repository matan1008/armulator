from armulator.opcodes.abstract_opcodes.bkpt import Bkpt
from armulator.opcodes.opcode import Opcode
from bitstring import BitArray


class BkptA1(Bkpt, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Bkpt.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = BitArray(bin="0000000000000000" + instr.bin[12:24] + instr.bin[-4:])
        if instr.bin[0:4] != "1110":
            print "unpredictable"
        else:
            return BkptA1(instr)
