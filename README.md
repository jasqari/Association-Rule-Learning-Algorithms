## Overview
This repository provides Python implementations of some of the popular association rule learning algorithms.
* `Algorithms/` contains:
    * Implementation of the Apriori algorithm and two of its variants, namely AprioriClose and Direct Hashing and Pruning (DHP)
    * Implementation of the Eclat algorithm
    * Implementation of the FP-growth algorithm
* `Data/` contains:
    * Two datasets comprised of genetic mutations in normal and overweight populations.

## Usage
See a full list of options:
```
python3 main.py -h
```

Specify the dataset, algorithm, and minimum support to find frequent itemsets:
```
python3 main.py normal apriori_close 5 
```