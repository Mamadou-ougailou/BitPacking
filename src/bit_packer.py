from abc import ABC, abstractmethod

class BitPacker(ABC):
    def __init__(self):
        self.n = 0  
        self.k = 0  
        self.compressed = []  
        self.compressionTime = "0.0000"
        self.decompressionTime = "0.0000"
        self.accessTime = "0.0000"

    @abstractmethod
    def compress(self, arr):
        pass

    @abstractmethod
    def decompress(self, output):
        pass

    @abstractmethod
    def get(self, i):
        pass

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