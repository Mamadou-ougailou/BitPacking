from BitPacking import BitPacking

if __name__ == "__main__":
    b = BitPacking()
    b1 = b.create("Version1")
    b1.compress(4)
    b1.decompress([])
    b2 = b.create("Version2")
    
    b2.compress(4)
    b2.decompress([])
