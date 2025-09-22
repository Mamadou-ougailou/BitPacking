import math
import datetime

class BitPackingVersion1:   
    def __init__(self):
        self.n = 0
        self.k = 0
        self.compressed = []
        self.compressionTime = 0
        self.decompressionTime = 0
        self.accessTime = 0
        
    def compress(self, arr):
        start_time = datetime.datetime.now()
        if(arr != [] and max(arr)!=0):
            self.n = len(arr)
            max_val = max(arr)
            self.k = max(1, math.ceil(math.log2(max_val + 1)))  
        
            out_size = math.ceil(self.n * self.k / 32)
            self.compressed = [0]*out_size
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
                    self.compressed[out_idx] |= (high_bits << (32 - bits_left))
                    out_idx += 1
                    low_bits = val & ((1 << (self.k - bits_left)) - 1)
                    if out_idx < len(self.compressed): 
                        self.compressed[out_idx] |= (low_bits << (32 - (bit_pos + self.k) % 32))
                    bit_pos += self.k
            
        else:
            self.n = 0
            self.k = 0
            self.compressionTime = 0.0000
            self.compressed = []
        
        total_time = datetime.datetime.now() - start_time
        self.compressionTime =  format(total_time.total_seconds()*1000, '.4f')

        return self.compressed         


    def decompress(self, output):
        start_time = datetime.datetime.now()
        if self.n != 0 and self.k != 0 :
            output = [0]*self.n
            bit_pos = 0
            for i in range(self.n):
                start_idx = bit_pos // 32
                start_bit = bit_pos % 32
                bits_left = 32 - start_bit
                
                if bits_left >= self.k:
                    output[i] = (self.compressed[start_idx] >> (bits_left - self.k)) & ((1 << self.k) - 1)
                else:
                    high_bits = ((self.compressed[start_idx] >> (32 - bits_left)) & ((1 << bits_left) - 1)) << (self.k - bits_left)
                    if start_idx + 1 < len(self.compressed):
                        low_bits = self.compressed[start_idx + 1] >> (32 - (self.k - bits_left))
                        low_bits &= (1 << (self.k - bits_left)) - 1
                    output[i] = high_bits | low_bits
                bit_pos += self.k
            total_time = datetime.datetime.now() - start_time
            self.decompressionTime = format(total_time.total_seconds() * 1000, '.4f')
        else:
            output = []
            self.decompressionTime = 0.0000

        return output



    def get(self, i):
        start_time = datetime.datetime.now()
        if i >= 0 and i < self.n:

            bit_pos = i * self.k
            start_idx = bit_pos // 32
            start_bit = bit_pos % 32
            bits_left = 32 - start_bit
            number = 0
            
            if bits_left >= self.k:
                number = self.compressed[start_idx] >> (bits_left - self.k) & ((1 << self.k) - 1)
            else:
                high_bits = ((self.compressed[start_idx] >> (32 - bits_left)) & ((1 << bits_left) - 1)) << (self.k - bits_left)
                if start_idx + 1 < len(self.compressed):
                    low_bits = self.compressed[start_idx + 1] >> (32 - (self.k - bits_left))
                number =  high_bits | (low_bits & ((1 << (self.k - bits_left)) - 1))
            total_time = datetime.datetime.now() - start_time
            self.accessTime = format(total_time.total_seconds() * 1000, '.4f')
            return number
        else:
            self.accessTime = 0.0000
            raise IndexError("Index out of bounds")
    
    def getCompressionTime(self):
            return self.compressionTime
    
    
    def getDecompressionTime(self):
            return self.decompressionTime
    
    
    def getAccesTime(self):
            return self.accessTime