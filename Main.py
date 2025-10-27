import sys
import random
from src.bit_packing_factory import BitPackingFactory

def print_menu():
    print("\n--- Bit Packing Project Menu ---")
    print("1. Compress an array")
    print("2. Decompress the current compressed array")
    print("3. Get a value at index from compressed array")
    print("4. View compression/decompression times")
    print("5. Calculate latency threshold")
    print("6. Generate random array")
    print("7. Switch version")
    print("8. Exit")
    print("--------------------------------")

def main():
    version_types = {
        "1": "Version1",
        "2": "Version2",
        "3": "Overflow"
    }
    current_type = "Version1"
    bp = BitPackingFactory().create(current_type)
    
    arr = None
    compressed = None
    output = None
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == "1":
            if arr is None:
                print("No array loaded. Generate one first (option 6).")
                continue
            compressed = bp.compress(arr)
            print(f"Compressed array: {compressed}")
            print(f"Compression time: {bp.getCompressionTime()} ms")
        
        elif choice == "2":
            if compressed is None:
                print("Compress an array first (option 1).")
                continue
            size = len(arr) if arr else 0
            output = [0] * size
            decompressed = bp.decompress(output)
            print(f"Decompressed array: {decompressed}")
            print(f"Decompression time: {bp.getDecompressionTime()} ms")
        
        elif choice == "3":
            if compressed is None:
                print("Compress an array first (option 1).")
                continue
            try:
                i = int(input("Enter index: "))
                val = bp.get(i)
                print(f"Value at index {i}: {val}")
                print(f"Access time: {bp.getAccessTime()} ms")
            except ValueError:
                print("Invalid index.")
            except IndexError as e:
                print(e)
        
        elif choice == "4":
            print(f"Compression time: {bp.getCompressionTime()} ms")
            print(f"Decompression time: {bp.getDecompressionTime()} ms")
        
        elif choice == "5":
            t = bp.calculate_latency_threshold()
            if t is not None:
                print(f"Latency threshold: {t:.10f} s/byte")
            else:
                print("N/A (no compression benefit)")
        
        elif choice == "6":
            try:
                size = int(input("Enter array size: "))
                min_val = int(input("Enter min value: "))
                max_val = int(input("Enter max value: "))
                arr = [random.randint(min_val, max_val) for _ in range(size)]
                print(f"Generated array: {arr[:10]}... (showing first 10)")
            except ValueError:
                print("Invalid input.")
        
        elif choice == "7":
            print("Available versions:")
            for key in version_types:
                print(f"{key}. {version_types[key]}")
            selected = input("Select version (1-3): ").strip()
            if selected in version_types:
                current_type = version_types[selected]
                bp = BitPackingFactory().create(current_type)
                print(f"Switched to {current_type}")
                # Reset data on switch
                compressed = None
                output = None
            else:
                print("Invalid choice.")
        
        elif choice == "8":
            print("Exiting...")
            sys.exit(0)
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()