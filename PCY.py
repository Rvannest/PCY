import time
from collections import defaultdict

# hash function
def hash_function(x, y, num_buckets):
    return (x + y) % num_buckets

baskets = []

# path data file
data_file_path = ""

# Open read data file
with open(data_file_path, 'r') as file:
    for line in file:
        # Split the line into integers, create basket
        single_basket = [int(item) for item in line.strip().split()]
        baskets.append(single_basket)

#PCY function
def pcy(baskets, support_threshold, num_buckets):
    bucket_counts = defaultdict(int)
    singleton_counts = defaultdict(int)

    #First pass
    for basket in baskets:
        for i in basket:
            singleton_counts[i] += 1
            for j in basket:
                if i < j:
                    bucket = hash_function(i, j, num_buckets)
                    bucket_counts[bucket] += 1

    #create bitmap
    bitmap = {k: 1 for k, v in bucket_counts.items() if v >= support_threshold}

    # second pass
    frequent_pairs = set()
    for basket in baskets:
        for i in basket:
            for j in basket:
                if i < j and (i, j) in bitmap and singleton_counts[i] >= support_threshold and singleton_counts[j] >= support_threshold:
                    frequent_pairs.add((i, j))

    return frequent_pairs

# chunk sizes and thresholds
chunk_sizes = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
thresholds = [1, 5, 10]  # 1%, 5% thresholds
num_buckets = 10013  #value based on available memory

#PCY algorithm all chunk size and threshold
for support_threshold_percentage in thresholds:
    for chunk_size in chunk_sizes:
        # Calculate actual support threshold
        support_threshold = (len(baskets) * support_threshold_percentage) / 100

        # Select chunk of dataset to use
        baskets_chunk = baskets[:int(len(baskets) * chunk_size)]

        # execution time
        start_time = time.time()

        # Run PCY on selected chunk
        frequent_itemsets = pcy(baskets_chunk, support_threshold, num_buckets)

        # execution time in milliseconds
        execution_time = (time.time() - start_time) * 1000
        print(f"Execution Time: {execution_time:.2f} ms with a chunk size of {chunk_size:.2f} and {support_threshold_percentage}% threshold")

        print(f"Frequent Itemsets: {frequent_itemsets}\n")
