import time
import math
from src.bit_packer import BitPacker

class BitPackingVersion2(BitPacker):
    def __init__(self):
        super().__init__()

    def compress(self, arr):
        """Compresse un tableau d'entiers avec alignement sur mots."""
        start_time = time.perf_counter()
        if arr and max(abs(v) for v in arr) != 0:
            self.n = len(arr)
            max_val = max(abs(v) for v in arr)
            # include sign bit like Version1 so negative numbers are represented
            self.k = max(1, math.ceil(math.log2(max_val + 1)) + 1)
            if self.k > 32:
                raise ValueError("Bit width k > 32 not supported")

            values_per_word = 32 // self.k 
            out_size = math.ceil(self.n / values_per_word)
            self.compressed = [0] * out_size

            word_idx = 0
            used_bits_in_word = 0  

            mask = (1 << self.k) - 1

            for val in arr:
                val &= mask
                bits_left = 32 - used_bits_in_word

                if bits_left < self.k:
                    word_idx += 1
                    used_bits_in_word = 0
                    bits_left = 32

                shift = bits_left - self.k
                self.compressed[word_idx] |= (val << shift)
                used_bits_in_word += self.k

                if used_bits_in_word == 32:
                    word_idx += 1
                    used_bits_in_word = 0
            
            self.compressionTime = format((time.perf_counter() - start_time) * 1000, '.4f')
        else:
            self.n = 0
            self.k = 0
            self.compressionTime = "0.0000"
            self.compressed = []
        return self.compressed

    def decompress(self, output):
        """Décompresse dans le tableau output (pré-alloué de taille n)."""
        start_time = time.perf_counter()
        if self.n != 0 and self.k != 0:
            if len(output) < self.n:
                raise ValueError("Output array too small")

            values_per_word = 32 // self.k
            mask = (1 << self.k) - 1

            for i in range(self.n):
                word_idx = i // values_per_word
                pos_in_word = i % values_per_word
                bits_left = 32 - pos_in_word * self.k
                shift = bits_left - self.k
                output[i] = (self.compressed[word_idx] >> shift) & mask
                if output[i] & (1 << (self.k - 1)):
                    output[i] -= (1 << self.k)
            self.decompressionTime = format((time.perf_counter() - start_time) * 1000, '.4f')
        else:
            output = []
            self.decompressionTime = "0.0000"
        return output

    def get(self, i):
        """Accès aléatoire à l'élément i."""
        start_time = time.perf_counter()
        if 0 <= i < self.n:
            values_per_word = 32 // self.k
            mask = (1 << self.k) - 1

            word_idx = i // values_per_word
            pos_in_word = i % values_per_word
            bits_left = 32 - pos_in_word * self.k
            shift = bits_left - self.k
            number = (self.compressed[word_idx] >> shift) & mask
            if number & (1 << (self.k - 1)):
                number -= (1 << self.k)
            self.accessTime = format((time.perf_counter() - start_time) * 1000, '.4f')
            return number
        else:
            self.accessTime = "0.0000"
            raise IndexError("Index out of bounds")

  