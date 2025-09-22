from BitPacking import BitPacking

if __name__ == "__main__":
    b1 = BitPacking().create("Version1")
    b2 = BitPacking().create("Version2")
    #array = [1,2, 3, 5, 10, 6, 2, 20, 4, 23, 24, 14, 16, 27, 31, 7, 30,12, 9, 7]
    array = [2024]* 100000000
    compressedArray = b1.compress(array)
    #print(compressedArray)
    print(b1.getCompressionTime())
   # v2compressedArray = b2.compress(array)
    #print(b2.getCompressionTime())
    #print(b2.decompress([]))
 