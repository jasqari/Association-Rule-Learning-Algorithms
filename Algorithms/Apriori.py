from itertools import combinations
from collections import defaultdict


def frequent_item_set(item_sets, trans_database, min_support):
    frequency_dict = dict.fromkeys(item_sets, 0)
    for item_set in item_sets:
        for _, value in trans_database.items():
            if item_set.issubset(value):
                frequency_dict[item_set] += 1
    frequency_dict = {key: value for key, value in frequency_dict.items() if value >= min_support}

    return frequency_dict


def self_join(item_set, k):
    items = frozenset(item_set.keys())
    candidates = []
    for item1 in items:
        for item2 in items:
            combination = item1.union(item2)
            if len(combination) == k:
                candidates.append(combination)

    return set(candidates)


def prune(cand_itemsets_k, freq_itemsets_k_prev, k):
    pruned_cand_itemsets_k = set()
    for item_set in cand_itemsets_k:
        pruned_cand_itemsets_k.add(item_set)
    for item_set in cand_itemsets_k:
        for k_minus_one_itemset in combinations(item_set, k - 1):
            if not (frozenset(k_minus_one_itemset) in freq_itemsets_k_prev):
                pruned_cand_itemsets_k.remove(item_set)
                break
    return pruned_cand_itemsets_k


def apriori(database, min_support):
    transactional = defaultdict(list)
    for row in database:
        mutation = row[0]
        pid = row[1]
        transactional[pid].append(mutation)
    transactional.update((key, frozenset(value)) for key, value in transactional.items())

    all_freq_itemsets = {}
    k = 1
    cand_itemsets_k = set([frozenset({row[0]}) for row in database])
    freq_itemsets_k = frequent_item_set(cand_itemsets_k, transactional, min_support)
    all_freq_itemsets.update(freq_itemsets_k)
    k += 1

    while freq_itemsets_k:
        freq_itemsets_k_prev = freq_itemsets_k
        cand_itemsets_k = prune(self_join(freq_itemsets_k_prev, k), freq_itemsets_k_prev, k)
        freq_itemsets_k = frequent_item_set(cand_itemsets_k, transactional, min_support)
        all_freq_itemsets.update(freq_itemsets_k)
        k += 1

    return all_freq_itemsets


def partition(database, min_support, num_partitions):
    partitions = [
        database[
            int(i * (len(database) / num_partitions)) : int(
                (i + 1) * (len(database) / num_partitions)
            )
        ]
        for i in range(num_partitions)
    ]

    all_cand_itemsets = {}
    for partition in partitions:
        partition_freq_itemsets = apriori(partition, min_support / num_partitions)
        all_cand_itemsets.update(partition_freq_itemsets)

    transactional = defaultdict(list)
    for row in database:
        mutation = row[0]
        pid = row[1]
        transactional[pid].append(mutation)
    transactional.update((key, frozenset(value)) for key, value in transactional.items())

    all_freq_itemsets = frequent_item_set(all_cand_itemsets.keys(), transactional, min_support)

    return all_freq_itemsets
