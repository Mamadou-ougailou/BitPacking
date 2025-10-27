from .versions.bit_packing_verion1 import BitPackingVersion1
from .versions.bit_packing_version2 import BitPackingVersion2
from .versions.bit_packing_overflow import BitPackingOverflow

class BitPackingFactory:
    @staticmethod
    def create(type):

        versions ={
            "Version1": BitPackingVersion1,
            "Version2": BitPackingVersion2,
            "Overflow": BitPackingOverflow
        }
        if type not in versions:
            raise KeyError(f"Type inconnu : {type}. Types valides : {list(versions.keys())}")
        return versions[type]()
