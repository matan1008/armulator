from abc import ABCMeta, abstractmethod


class AbstractOpcode(object):
    """
     Abstract Opcode class
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kw):
        pass

    @abstractmethod
    def execute(self, processor):
        """ Execute the opcode on the given processor
        :param processor:
        """
        pass
