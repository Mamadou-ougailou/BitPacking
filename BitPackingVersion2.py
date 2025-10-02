import math
import time

class BitPackingVersion2:
    
    def __init__(self):
        self.n = 0
        self.k = 0
        self.compressed = []
        self.compressionTime = 0
        self.decompressionTime = 0
        self.accessTime = 0
        

    def compress(self, arr):
        start_time = time.perf_counter()

        if(arr != [] and max(arr)!=0):
            self.n = len(arr)
            max_val = max(arr)
            self.k = max(1, math.ceil(math.log2(max_val + 1)))

            if self.k > 32:
                raise ValueError(f"k = {self.k} > 32 : impossible de stocker un entier compressé entièrement "
                                "dans un mot de 32 bits sans le découper.")

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
            
            total_time = time.perf_counter() - start_time
            self.compressionTime = format(total_time * 1000, '.4f')
        else:
            self.n = 0
            self.k = 0
            self.compressionTime = "0.0000"
            self.compressed = []

        return self.compressed

    def decompress(self, output):
        start_time = time.perf_counter()

        if self.n != 0 and self.k != 0 and len(output) >= self.n:

            values_per_word = 32 // self.k
            mask = (1 << self.k) - 1
            #output = [0] * self.n

            for i in range(self.n):
                word_idx = i // values_per_word
                pos_in_word = i % values_per_word
                bits_left = 32 - pos_in_word * self.k
                shift = bits_left - self.k
                output[i] = (self.compressed[word_idx] >> shift) & mask

            total_time = time.perf_counter() - start_time
            self.decompressionTime = format(total_time * 1000, '.4f')
        else:
            output = []
            self.decompressionTime = "0.0000"
        return output

    def get(self, i):
        start_time = time.perf_counter()
        if i >= 0 and i < self.n :
            values_per_word = 32 // self.k
            mask = (1 << self.k) - 1

            word_idx = i // values_per_word
            pos_in_word = i % values_per_word
            bits_left = 32 - pos_in_word * self.k
            shift = bits_left - self.k
            number = (self.compressed[word_idx] >> shift) & mask

            total_time = time.perf_counter() - start_time
            self.accessTime = format(total_time * 1000, '.4f')
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

