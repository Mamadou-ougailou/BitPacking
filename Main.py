from BitPacking import BitPacking
from Utils import generate_input, run_with_averaging

if __name__ == "__main__":
    b1 = BitPacking().create("Version1")
    b2 = BitPacking().create("Version2")
    max = 10000 
    size = 10
    array = generate_input(size, max)
    print(array)
    arrayDec = [0]*size


    comp_array1, decomp_array1, avg_comp_time1, avg_decomp_time1 = run_with_averaging(b1, array)
    comp_array2, decomp_array2, avg_comp_time2, avg_decomp_time2 = run_with_averaging(b2, array)

    print(comp_array1)
    print(comp_array2)

    print(f"Version 1 - Average Compression Time: {avg_comp_time1:.4f} ms, Average Decompression Time: {avg_decomp_time1:.4f} ms")
    print(f"Version 2 - Average Compression Time: {avg_comp_time2:.4f} ms, Average Decompression Time: {avg_decomp_time2:.4f} ms")
    t1 = b1.calculate_latency_threshold()
    if t1 is not None:
        print(f"Version1 Latency Threshold t: {t1:.10f} seconds/byte")
        print(f"  (Compression worthwhile if transmission latency per byte > {t1:.10f} s/byte)")
    else:
        print("Version1: Compression does not reduce size.")

    t2 = b2.calculate_latency_threshold()
    if t2 is not None:
        print(f"Version2 Latency Threshold t: {t2:.10f} seconds/byte")
        print(f"  (Compression worthwhile if transmission latency per byte > {t2:.10f} s/byte)")
    else:
        print("Version2: Compression does not reduce size.")

    print("Are they equal? " + str(decomp_array1 == array and decomp_array2 == array))