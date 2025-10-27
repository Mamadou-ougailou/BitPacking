
from src.versions.bit_packing_verion1 import BitPackingVersion1
from src.versions.bit_packing_version2 import BitPackingVersion2
from src.versions.bit_packing_overflow import BitPackingOverflow
from src.utils import run_with_averaging, generate_input
import statistics
import random

def benchmark_versions(sizes, k_values, runs=3):
    """
    Benchmark all three versions for given sizes and k_values.
    Returns a list of dicts for table rows.
    """
    results = []
    versions = [
        ("Version1", BitPackingVersion1),
        ("Version2", BitPackingVersion2),
        ("Overflow", BitPackingOverflow),
    ]
    
    for size in sizes:
        for k in k_values:
            min_val = -(1 << (k - 1))
            max_val = (1 << (k - 1)) - 1
            array = generate_input(size, min_val, max_val)
            
            for name, cls in versions:
                bp = cls()
                compressed, decompressed, avg_compress, avg_decompress = run_with_averaging(bp, array, runs)
                
                # Memory usage
                mem_bytes = len(compressed) * 4
                
                # Random access benchmark
                get_times = []
                for _ in range(runs):
                    random_i = random.randint(0, size - 1)
                    _ = bp.get(random_i)
                    get_times.append(float(bp.getAccessTime()))
                avg_get = statistics.mean(get_times)
                
                # Latency threshold
                t_threshold = bp.calculate_latency_threshold()
                t_str = f"{t_threshold:.10f}" if t_threshold else "N/A"
                
                results.append({
                    "Size": size,
                    "k": k,
                    "Version": name,
                    "Compress (ms)": f"{avg_compress:.4f}",
                    "Decompress (ms)": f"{avg_decompress:.4f}",
                    "Get (ms)": f"{avg_get:.4f}",
                    "Memory (B)": mem_bytes,
                    "Latency Threshold (s/byte)": t_str
                })
    
    return results

def print_table(results):
    """Print results as a Markdown table."""
    if not results:
        print("No results.")
        return
    
    headers = list(results[0].keys())
    print("| " + " | ".join(headers) + " |")
    print("| " + "--- | " * len(headers))
    
    for row in results:
        print("| " + " | ".join(str(row[h]) for h in headers) + " |")

if __name__ == "__main__":
    sizes = [10, 100, 1000, 10000]
    k_values = [4, 8, 16, 32]
    results = benchmark_versions(sizes, k_values, runs=5)
    print_table(results)
