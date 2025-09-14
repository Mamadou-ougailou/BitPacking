from BitPackingVersion1 import BitPackingVersion1
from BitPackingVersion2 import BitPackingVersion2

class BitPacking:
    @staticmethod
    def create(type):

        versions ={
            "Version1": BitPackingVersion1,
            "Version2": BitPackingVersion2
        }

        return versions[type]()
