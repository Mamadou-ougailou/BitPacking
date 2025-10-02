import math
import time

class BitPackingVersion1:
    def __init__(self):
        self.n = 0  
        self.k = 0  
        self.compressed = []  
        self.compressionTime = "0.0000"
        self.decompressionTime = "0.0000"
        self.accessTime = "0.0000"

    def compress(self, arr):
        """Compresse un tableau d'entiers en utilisant un packing serré."""
        start_time = time.perf_counter()
        if arr and max(arr) != 0:
            self.n = len(arr)
            max_val = max(arr)
            self.k = max(1, math.ceil(math.log2(max_val + 1)))
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
                else:
                    high_bits = (self.compressed[start_idx] & ((1 << bits_left) - 1)) << (self.k - bits_left)
                    low_bits = 0
                    if start_idx + 1 < len(self.compressed):
                        low_bits = self.compressed[start_idx + 1] >> (32 - (self.k - bits_left))
                        low_bits &= (1 << (self.k - bits_left)) - 1
                    output[i] = high_bits | low_bits
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
            else:
                high_bits = (self.compressed[start_idx] & ((1 << bits_left) - 1)) << (self.k - bits_left)
                low_bits = 0
                if start_idx + 1 < len(self.compressed):
                    low_bits = self.compressed[start_idx + 1] >> (32 - (self.k - bits_left))
                    low_bits &= (1 << (self.k - bits_left)) - 1
                number = high_bits | low_bits
            self.accessTime = format((time.perf_counter() - start_time) * 1000, '.4f')
            return number
        else:
            self.accessTime = "0.0000"
            raise IndexError("Index out of bounds")

    def getCompressionTime(self):
        return self.compressionTime

    def getDecompressionTime(self):
        return self.decompressionTime

    def getAccessTime(self):
        return self.accessTime
    
    def calculate_latency_threshold(self):
        if self.n == 0 or self.k == 0:
            return None
        
        S_u = self.n * 4  # bytes, uncompressed
        S_c = len(self.compressed) * 4  # bytes, compressed
        if S_c >= S_u:
            return None  # Compression not beneficial
        
        # Convert times from ms strings to seconds floats
        time_c = float(self.compressionTime) / 1000
        time_d = float(self.decompressionTime) / 1000
        
        t_threshold = (time_c + time_d) / (S_u - S_c)
        return t_threshold