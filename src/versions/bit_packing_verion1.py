import math
import time
from src.bit_packer import BitPacker

class BitPackingVersion1(BitPacker):
    def __init__(self):
        super().__init__()

    def compress(self, arr):
        start_time = time.perf_counter()
        if arr and max(abs(v) for v in arr) != 0:
            self.n = len(arr)
            max_val = max(abs(v) for v in arr)
            self.k = max(1, math.ceil(math.log2(max_val + 1)) + 1)
            if self.k > 32:
                raise ValueError("Bit width k > 32 not supported")

            out_size = math.ceil(self.n * self.k / 32)
            self.compressed = [0] * out_size
            bit_pos = 0
            out_idx = 0

            for val in arr:
                val &= (1 << self.k) - 1  
                bits_left = 32 - (bit_pos % 32)
                if bits_left >= self.k:
                    self.compressed[out_idx] |= (val << (bits_left - self.k))
                    bit_pos += self.k
                    if bit_pos % 32 == 0:
                        out_idx += 1
                else:
                    high_bits = val >> (self.k - bits_left)
                    self.compressed[out_idx] |= high_bits
                    out_idx += 1
                    low_bits = val & ((1 << (self.k - bits_left)) - 1)
                    if out_idx < len(self.compressed):
                        self.compressed[out_idx] |= (low_bits << (32 - (bit_pos + self.k) % 32))
                    bit_pos += self.k

            self.compressionTime = format((time.perf_counter() - start_time) * 1000, '.4f')
        else:
            self.n = 0
            self.k = 0
            self.compressionTime = "0.0000"
            self.compressed = []
        return self.compressed

    def decompress(self, output):
        start_time = time.perf_counter()
        if self.n != 0 and self.k != 0:
            if len(output) < self.n:
                raise ValueError("Output array too small")
            bit_pos = 0
            for i in range(self.n):
                start_idx = bit_pos // 32
                start_bit = bit_pos % 32
                bits_left = 32 - start_bit

                if bits_left >= self.k:
                    output[i] = (self.compressed[start_idx] >> (bits_left - self.k)) & ((1 << self.k) - 1)
                    if output[i] & (1 << (self.k - 1)):
                        output[i] -= (1 << self.k)
                else:
                    high_bits = (self.compressed[start_idx] & ((1 << bits_left) - 1)) << (self.k - bits_left)
                    low_bits = 0
                    if start_idx + 1 < len(self.compressed):
                        low_bits = self.compressed[start_idx + 1] >> (32 - (self.k - bits_left))
                        low_bits &= (1 << (self.k - bits_left)) - 1
                    output[i] = high_bits | low_bits
                    if output[i] & (1 << (self.k - 1)):
                        output[i] -= (1 << self.k)
                bit_pos += self.k
            self.decompressionTime = format((time.perf_counter() - start_time) * 1000, '.4f')
        else:
            output = []
            self.decompressionTime = "0.0000"
        return output

    def get(self, i):
        """Accès aléatoire à l'élément i."""
        start_time = time.perf_counter()
        if 0 <= i < self.n:
            bit_pos = i * self.k
            start_idx = bit_pos // 32
            start_bit = bit_pos % 32
            bits_left = 32 - start_bit

            if bits_left >= self.k:
                number = (self.compressed[start_idx] >> (bits_left - self.k)) & ((1 << self.k) - 1)
                if number & (1 << (self.k - 1)):
                    number -= (1 << self.k)
            else:
                high_bits = (self.compressed[start_idx] & ((1 << bits_left) - 1)) << (self.k - bits_left)
                low_bits = 0
                if start_idx + 1 < len(self.compressed):
                    low_bits = self.compressed[start_idx + 1] >> (32 - (self.k - bits_left))
                    low_bits &= (1 << (self.k - bits_left)) - 1
                number = high_bits | low_bits
                if number & (1 << (self.k - 1)):
                    number -= (1 << self.k)
            self.accessTime = format((time.perf_counter() - start_time) * 1000, '.4f')
            return number
        else:
            self.accessTime = "0.0000"
            raise IndexError("Index out of bounds")
