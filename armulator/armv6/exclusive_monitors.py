from bitstring import BitArray
from armulator.armv6.bits_ops import add
from armulator.armv6.configurations import configurations


class ExclusiveRecord(object):
    def __init__(self, paddress, processorid, size):
        self.paddress = paddress
        self.processorid = processorid
        self.size = size

    def is_in_block(self, paddress):
        return self.paddress.uint <= paddress.uint < self.paddress.uint + self.size

    def is_end_in_block(self, paddress, size):
        end = add(paddress, BitArray(uint=size, length=len(paddress)), len(paddress))
        return self.is_in_block(end)


class LocalExclusiveMonitor(object):
    """Monitors exclusive accesses to memory"""

    def __init__(self, erg):
        self.erg = erg
        self.records = []

    def is_exclusive(self, paddress, processorid, size):
        address = paddress.physicaladdress
        for record in self.records:
            if record.processorid == processorid and record.is_in_block(address):
                if record.is_end_in_block(address, size) or configurations.impdef_is_exclusive_not_cover_all_size:
                    return True
        return False

    def mark_exclusive(self, paddress, processorid, size):
        record = ExclusiveRecord(
                paddress.physicaladdress[:-self.erg] + BitArray(length=self.erg),
                processorid,
                max(2 ** self.erg, size)
        )
        self.records.append(record)

    def clear_exclusive(self, proceesorid):
        self.records = filter(lambda record: record.processorid != proceesorid, self.records)


class GlobalExclusiveMonitor(object):
    """Monitors exclusive accesses to memory"""

    def __init__(self, erg):
        self.erg = erg
        self.records = []

    def is_exclusive(self, paddress, processorid, size):
        address = paddress.physicaladdress
        for record in self.records:
            if (record.processorid == processorid and
                    record.is_in_block(address) and
                    record.is_end_in_block(address, size)):
                return True
        return False

    def mark_exclusive(self, paddress, processorid, size):
        record = ExclusiveRecord(
                paddress.physicaladdress[:-self.erg] + BitArray(length=self.erg),
                processorid,
                max(2 ** self.erg, size)
        )
        for index in xrange(len(self.records)):
            if self.records[index].processorid == processorid:
                self.records[index] = record
                return
        self.records.append(record)

    def clear_exclusive_by_address(self, paddress, processorid, size):
        records = []
        for record in self.records:
            if record.is_in_block(paddress.physicaladdress):
                if processorid != record.processorid or configurations.impdef_gexclusive_clear_cur_processor:
                    continue
            records.append(record)
        self.records = records
