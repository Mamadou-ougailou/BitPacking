import random
import statistics
from src.versions.bit_packing_verion1 import BitPackingVersion1
from src.versions.bit_packing_version2 import BitPackingVersion2
from src.versions.bit_packing_overflow import BitPackingOverflow


def run_with_averaging(bp, array, runs=5):
    compression_times = []
    decompression_times = []
    size = len(array)
    arrayDec = [0]*size

    for _ in range(runs):
        compresed_array = bp.compress(array)
        compression_times.append(float(bp.getCompressionTime()))

        decompressed_array = bp.decompress(arrayDec)
        decompression_times.append(float(bp.getDecompressionTime()))
    

    avg_compression_time = statistics.mean(compression_times)
    avg_decompression_time = statistics.mean(decompression_times)

    return compresed_array, decompressed_array, avg_compression_time, avg_decompression_time

def generate_input(size, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(size)]
