import unittest
import math
import random

from src.versions.bit_packing_verion1 import BitPackingVersion1
from src.versions.bit_packing_version2 import BitPackingVersion2
from src.versions.bit_packing_overflow import BitPackingOverflow

class TestBitPackingVersions(unittest.TestCase):

    def setUp(self):
        self.versions = [
            BitPackingVersion1,
            BitPackingVersion2,
            BitPackingOverflow
        ]
        self.test_cases = [
            # Empty array
            [],
            # All zeros
            [0] * 10,
            # Positive small values
            [1, 2, 3, 4, 5],
            # Large positive values
            [1023, 2047, 4095],
            # Negative values
            [-1, -2, -3, 1, 2, 3],
            # Mixed signed with outliers
            [1, 2, 3, -1024, 4, 5, 2048, -2048],
            # Edge: min/max for k=10 signed
            [-(1 << 9), (1 << 9) - 1, 0],
            # Random medium array
            [random.randint(-100, 100) for _ in range(100)],
        ]

    def test_compress_decompress_roundtrip(self):
        for version in self.versions:
            for arr in self.test_cases:
                with self.subTest(version=version.__name__, arr=arr):
                    bp = version()
                    compressed = bp.compress(arr)
                    output = [0] * len(arr)
                    decompressed = bp.decompress(output)
                    if len(arr) == 0 or all(v == 0 for v in arr):
                        self.assertEqual(decompressed, [], f"Roundtrip failed for {version.__name__}")
                    else:
                        self.assertEqual(decompressed, arr, f"Roundtrip failed for {version.__name__}")

    def test_get_random_access(self):
        for version in self.versions:
            for arr in self.test_cases:
                if not arr or all(v == 0 for v in arr):
                    continue  # Skip get for empty or all-zero (n=0)
                with self.subTest(version=version.__name__, arr=arr):
                    bp = version()
                    bp.compress(arr)
                    for i in range(len(arr)):
                        val = bp.get(i)
                        self.assertEqual(val, arr[i], f"Get failed at index {i} for {version.__name__}")
                    with self.assertRaises(IndexError):
                        bp.get(-1)
                    with self.assertRaises(IndexError):
                        bp.get(len(arr))

    def test_times_non_zero(self):
        for version in self.versions:
            arr = [1, 2, 3]
            bp = version()
            bp.compress(arr)
            output = [0] * len(arr)
            bp.decompress(output)
            bp.get(0)
            self.assertNotEqual(bp.getCompressionTime(), "0.0000", f"Compression time zero for {version.__name__}")
            self.assertNotEqual(bp.getDecompressionTime(), "0.0000", f"Decompression time zero for {version.__name__}")
            self.assertNotEqual(bp.getAccessTime(), "0.0000", f"Access time zero for {version.__name__}")

    def test_latency_threshold(self):
        for version in self.versions:
            arr = [1] * 100
            bp = version()
            bp.compress(arr)
            output = [0] * len(arr)
            bp.decompress(output)
            t = bp.calculate_latency_threshold()
            if t is not None:
                self.assertGreater(t, 0, f"Invalid threshold for {version.__name__}")
            else:
                self.fail(f"Threshold None for compressible array in {version.__name__}")

    def test_edge_cases(self):
        for version in self.versions:
            bp = version()
            # Empty
            self.assertEqual(bp.compress([]), [])
            self.assertEqual(bp.decompress([]), [])
            with self.assertRaises(IndexError):
                bp.get(0)
            # All zeros
            arr = [0] * 5
            compressed = bp.compress(arr)
            self.assertEqual(compressed, [])
            output = [0] * 5
            decompressed = bp.decompress(output)
            self.assertEqual(decompressed, [])
            # k > 32 error
            large_arr = [1 << 33]
            with self.assertRaises(ValueError):
                bp.compress(large_arr)
            # Overflow specific: no overflow
            if version == BitPackingOverflow:
                small_arr = [1, 2, 3]
                bp.compress(small_arr)
                self.assertEqual(bp.m, 0, "Overflow count should be 0 for small values")

if __name__ == '__main__':
    unittest.main()