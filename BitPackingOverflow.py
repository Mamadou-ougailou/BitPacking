import math
import time

class BitPackingOverflow:
    def __init__(self):
        self.n = 0
        self.k = 0
        self.k_prime = 0
        self.m = 0
        self.p = 0
        self.dim = 0
        self.w = 0
        self.compressionTime = "0.0000"
        self.decompressionTime = "0.0000"
        self.accessTime = "0.0000"
        self.compressed = []

    def compress(self, arr):
        start_time = time.perf_counter()
        if arr and max(abs(v) for v in arr) != 0:
            self.n = len(arr)
            max_val = max(abs(v) for v in arr)
            self.k = max(1, math.ceil(math.log2(max_val + 1)) + 1)
            best_total = self.n * self.k
            best_k_prime = self.k
            best_m = 0
            best_p = 0
            best_dim = self.k
            best_w = self.k
            best_large = []
            for k_prime in range(2, self.k):  # Start from 2 to have sign bit
                large = [v for v in arr if v < -(1 << (k_prime - 1)) or v >= (1 << (k_prime - 1))]
                m = len(large)
                p = math.ceil(math.log2(m + 1)) if m > 0 else 0
                dim = max(k_prime, p)
                w = 1 + dim if m > 0 else k_prime
                inline_bits = self.n * w
                overflow_bits = m * self.k
                total = inline_bits + overflow_bits
                if total < best_total:
                    best_total = total
                    best_k_prime = k_prime
                    best_m = m
                    best_p = p
                    best_dim = dim
                    best_w = w
                    best_large = large
            self.k_prime = best_k_prime
            self.m = best_m
            self.p = best_p
            self.dim = best_dim
            self.w = best_w
            out_size = math.ceil(best_total / 32)
            self.compressed = [0] * out_size
            bit_pos = 0
            out_idx = 0
            curr_overflow_idx = 0
            for val in arr:
                if val < -(1 << (self.k_prime - 1)) or val >= (1 << (self.k_prime - 1)):
                    flag = 1
                    data = curr_overflow_idx
                    curr_overflow_idx += 1
                else:
                    flag = 0
                    data = val & ((1 << self.k_prime) - 1)
                entry = (flag << self.dim) | (data & ((1 << self.dim) - 1))
                val = entry
                val &= (1 << self.w) - 1
                bits_left = 32 - (bit_pos % 32)
                if bits_left >= self.w:
                    self.compressed[out_idx] |= (val << (bits_left - self.w))
                    bit_pos += self.w
                    if bit_pos % 32 == 0:
                        out_idx += 1
                else:
                    high_bits = val >> (self.w - bits_left)
                    self.compressed[out_idx] |= high_bits
                    out_idx += 1
                    low_bits = val & ((1 << (self.w - bits_left)) - 1)
                    if out_idx < len(self.compressed):
                        self.compressed[out_idx] |= (low_bits << (32 - (bit_pos + self.w) % 32))
                    bit_pos += self.w
            # Pack overflow
            for val in best_large:
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
                if bits_left >= self.w:
                    entry = (self.compressed[start_idx] >> (bits_left - self.w)) & ((1 << self.w) - 1)
                else:
                    high_bits = (self.compressed[start_idx] & ((1 << bits_left) - 1)) << (self.w - bits_left)
                    low_bits = 0
                    if start_idx + 1 < len(self.compressed):
                        low_bits = self.compressed[start_idx + 1] >> (32 - (self.w - bits_left))
                        low_bits &= (1 << (self.w - bits_left)) - 1
                    entry = high_bits | low_bits
                bit_pos += self.w
                flag = entry >> self.dim
                data = entry & ((1 << self.dim) - 1)
                if flag == 0:
                    data = data & ((1 << self.k_prime) - 1)
                    if data & (1 << (self.k_prime - 1)):
                        data -= (1 << self.k_prime)
                    output[i] = data
                else:
                    overflow_bit_pos = self.n * self.w + data * self.k
                    o_start_idx = overflow_bit_pos // 32
                    o_start_bit = overflow_bit_pos % 32
                    o_bits_left = 32 - o_start_bit
                    if o_bits_left >= self.k:
                        output[i] = (self.compressed[o_start_idx] >> (o_bits_left - self.k)) & ((1 << self.k) - 1)
                    else:
                        high_bits = (self.compressed[o_start_idx] & ((1 << o_bits_left) - 1)) << (self.k - o_bits_left)
                        low_bits = 0
                        if o_start_idx + 1 < len(self.compressed):
                            low_bits = self.compressed[o_start_idx + 1] >> (32 - (self.k - o_bits_left))
                            low_bits &= (1 << (self.k - o_bits_left)) - 1
                        output[i] = high_bits | low_bits
                    if output[i] & (1 << (self.k - 1)):
                        output[i] -= (1 << self.k)
            self.decompressionTime = format((time.perf_counter() - start_time) * 1000, '.4f')
        else:
            output = []
            self.decompressionTime = "0.0000"
        return output

    def get(self, i):
        start_time = time.perf_counter()
        if 0 <= i < self.n:
            bit_pos = i * self.w
            start_idx = bit_pos // 32
            start_bit = bit_pos % 32
            bits_left = 32 - start_bit
            if bits_left >= self.w:
                entry = (self.compressed[start_idx] >> (bits_left - self.w)) & ((1 << self.w) - 1)
            else:
                high_bits = (self.compressed[start_idx] & ((1 << bits_left) - 1)) << (self.w - bits_left)
                low_bits = 0
                if start_idx + 1 < len(self.compressed):
                    low_bits = self.compressed[start_idx + 1] >> (32 - (self.w - bits_left))
                    low_bits &= (1 << (self.w - bits_left)) - 1
                entry = high_bits | low_bits
            flag = entry >> self.dim
            data = entry & ((1 << self.dim) - 1)
            if flag == 0:
                data = data & ((1 << self.k_prime) - 1)
                if data & (1 << (self.k_prime - 1)):
                    data -= (1 << self.k_prime)
                number = data
            else:
                overflow_bit_pos = self.n * self.w + data * self.k
                o_start_idx = overflow_bit_pos // 32
                o_start_bit = overflow_bit_pos % 32
                o_bits_left = 32 - o_start_bit
                if o_bits_left >= self.k:
                    number = (self.compressed[o_start_idx] >> (o_bits_left - self.k)) & ((1 << self.k) - 1)
                else:
                    high_bits = (self.compressed[o_start_idx] & ((1 << o_bits_left) - 1)) << (self.k - o_bits_left)
                    low_bits = 0
                    if o_start_idx + 1 < len(self.compressed):
                        low_bits = self.compressed[o_start_idx + 1] >> (32 - (self.k - o_bits_left))
                        low_bits &= (1 << (self.k - o_bits_left)) - 1
                    number = high_bits | low_bits
                if number & (1 << (self.k - 1)):
                    number -= (1 << self.k)
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