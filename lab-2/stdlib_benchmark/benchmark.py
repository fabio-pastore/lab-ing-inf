from random import randint, sample, choice
from time import perf_counter
import matplotlib.pyplot as plt
from datetime import datetime

NUM_TESTS = 10
BENCHMARK_STRUCTURE_SIZES = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
MAX_I32_VAL = 2147483648

def benchmark_ds(data_structure, lookup_list):
    start = perf_counter()
    # start benchmark timer
    for val in lookup_list: 
        if val in data_structure:
            pass
    end = perf_counter()
    # end benchmark timer
    return ((end - start) / NUM_TESTS) # return average search time

if __name__ == "__main__":

    list_times = []
    set_times = []
    dict_times = []
    print("[MAIN] Initiating benchmark.")
    begin = perf_counter()

    for size in BENCHMARK_STRUCTURE_SIZES:
        
        li = sample(range(0, MAX_I32_VAL), size)
        s = set(li)
        d = {key : None for key in s}

        values_to_find = [choice(li) for k in range(NUM_TESTS)]
        list_res = benchmark_ds(li, values_to_find)
        list_times.append(list_res)

        set_res = benchmark_ds(s, values_to_find)
        set_times.append(set_res)

        dict_res = benchmark_ds(d, values_to_find)
        dict_times.append(dict_res)

    end = perf_counter()
    elapsed_time = round((end - begin), 3)

    with open ("benchmark_results.txt", "w", encoding="UTF-8") as fout:

        curr_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fout.write("Benchmark results - " + curr_datetime + "\n")
        fout.write("\n")
        fout.write("All structures were tested on the following sizes: " + str(BENCHMARK_STRUCTURE_SIZES) + "\n")
        fout.write("List: " + str(list_times) + "\n")
        fout.write("Set: " + str(set_times) + "\n")
        fout.write("Dict: " + str(dict_times) + "\n")

    print("[MAIN] Benchmark complete (took " + str(elapsed_time) + " seconds). Displaying results.")

    plt.figure(figsize=(10, 6))
    
    plt.plot(BENCHMARK_STRUCTURE_SIZES, list_times, label=r'List - $\mathcal{O}(n)$', marker='o', linewidth=2)
    plt.plot(BENCHMARK_STRUCTURE_SIZES, set_times, label=r'Set - $\mathcal{O}(1)$', marker='s', linewidth=2)
    plt.plot(BENCHMARK_STRUCTURE_SIZES, dict_times, label=r'Dict - $\mathcal{O}(1)$', marker='^', linewidth=2)

    plt.xscale('log')
    plt.yscale('log')

    plt.title('Standard library benchmark: List VS Set VS Dict', fontsize=14, fontweight='bold')
    plt.xlabel('Number of items in structure', fontsize=12)
    plt.ylabel('Average search time (seconds)', fontsize=12)
    
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()
    
    plt.show()

    print("Process exited with status code (0)")
    exit(0)