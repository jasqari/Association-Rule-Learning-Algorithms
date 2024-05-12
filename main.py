import csv
import time
import argparse
from collections import defaultdict
from Algorithms import Apriori, DHP, AprioriClose, FPGrowth, Eclat


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dataset",
        type=str,
        choices=["normal", "overweight"],
        help="Data to mine frequent itemsets from",
    )
    parser.add_argument(
        "algorithm",
        type=str,
        choices=["apriori", "dhp", "apriori_close", "fpgrowth", "eclat"],
        help="Choice of frequent itemset mining algorithm",
    )
    parser.add_argument(
        "min_support",
        type=int,
        help="Threshold to find all the frequent itemsets that are in the database",
    )
    args = parser.parse_args()

    """Load the data"""
    data_path = "Data/LIHC-Normal.csv" if args.dataset == "normal" else "Data/LIHC-Overweight.csv"
    csvreader = csv.reader(open(data_path))
    data = [row for row in csvreader]
    head = data[0][0]
    tail = [[t.split("(")[0][:-1], t.split("(")[1][:-1]] for t in set([row[0] for row in data[1:]])]

    """Map strings to integers"""
    mutations_map = {}
    mid = 0
    for m in set([row[0] for row in tail]):
        mutations_map[m] = mid
        mid += 1
    pid_map = {}
    pid = 0
    for p in set([row[1] for row in tail]):
        pid_map[p] = pid
        pid += 1
    mapped_database = [[mutations_map[r[0]], pid_map[r[1]]] for r in tail]

    """Run the algorithm"""
    file = open(
        "frequent_itemsets_{}_{}_{}.txt".format(args.dataset, args.algorithm, args.min_support), "w"
    )
    inv_mutations_map = {v: k for k, v in mutations_map.items()}
    t1 = time.time()
    if args.algorithm in ["apriori", "dhp", "apriori_close"]:
        alg_map = {
            "apriori": Apriori.apriori,
            "dhp": DHP.apriori,
            "apriori_close": AprioriClose.apriori,
        }
        freq_sets = alg_map[args.algorithm](mapped_database, args.min_support)
        for k, v in freq_sets.items():
            for m in k:
                file.write("{} {}\n".format(inv_mutations_map[m], v))

    elif args.algorithm == "eclat":
        vertical = defaultdict(set)
        for row in mapped_database:
            mutation = row[0]
            pid = row[1]
            vertical[mutation].add(pid)
        freq_sets = dict()
        Eclat.eclat(sorted(vertical.items(), key=lambda x: len(x[1]), reverse=True), [], freq_sets)
        file.write(str([([inv_mutations_map[m] for m in k], v) for k, v in freq_sets.items()]))
        for k, v in freq_sets.items():
            for m in k:
                file.write("{} {}\n".format(inv_mutations_map[m], v))

    else:
        transactional = defaultdict(list)
        for row in mapped_database:
            mutation = row[0]
            pid = row[1]
            transactional[pid].append(mutation)
        transactional = [[value, 1] for _, value in transactional.items()]
        tree = FPGrowth.FPTree(transactional, 2)
        freq_sets = []
        tree.FPGrowth(set(), freq_sets)
        for ms in freq_sets:
            file.write("{}\n".format(str([inv_mutations_map[m] for m in ms])))
    t2 = time.time()
    print("Time:", t2 - t1)
    file.close()
