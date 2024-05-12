from collections import defaultdict


def frequent_item_set(item_sets, trans_database, min_support):
    frequency_dict = dict.fromkeys(item_sets, 0)
    for _, value in trans_database.items():
        for item_set in item_sets:
            if item_set.issubset(value):
                frequency_dict[item_set] += 1
    frequency_dict = {key: value for key, value in frequency_dict.items() if value >= min_support}
    return frequency_dict


class Node:
    def __init__(self, item, parent):
        self.item = item
        self.freq = 1
        self.parent_node = parent
        self.child_nodes = {}
        self.next_header_node = None


class FPTree:
    def __init__(self, database, min_support):
        self.db = database
        self.min_support = min_support
        self.header_table = self.header_table()
        self.Tree = self.tree()

    def header_table(self):
        table = defaultdict(int)
        for row in self.db:
            for item in row[0]:
                table[item] += row[1]

        table = {key: [value, None] for key, value in table.items() if value >= self.min_support}
        table = dict(sorted(table.items(), key=lambda x: x[1], reverse=True))

        return table

    def tree(self):
        root = Node(None, None)
        if not len(self.header_table):
            return root
        for row in self.db:
            current_node = root
            items = [item for item in row[0] if item in self.header_table]
            sorted_items = sorted(items, key=lambda x: self.header_table[x][0], reverse=True)
            for item in sorted_items:
                if item not in current_node.child_nodes:
                    child_node = Node(item, current_node)
                    current_node.child_nodes[item] = child_node
                    if not self.header_table[item][1]:
                        self.header_table[item][1] = child_node
                    else:
                        header_node = self.header_table[item][1]
                        while header_node.next_header_node:
                            header_node = header_node.next_header_node
                        header_node.next_header_node = child_node
                else:
                    current_node.child_nodes[item].freq += 1
                current_node = current_node.child_nodes[item]

        return root

    def FPGrowth(self, prefix_itemset, freq_itemsets):
        sorted_header_items = [key for key in self.header_table.keys()]
        for item in sorted_header_items:
            freq_itemset = prefix_itemset.copy()
            freq_itemset.add(item)
            freq_itemsets.append(freq_itemset)

            conditional_database = []
            current_node = self.header_table[item][1]
            while current_node:
                condition = []
                traverse_node = current_node
                while traverse_node.parent_node:
                    condition.append(traverse_node.item)
                    traverse_node = traverse_node.parent_node
                if len(condition) > 1:
                    conditional_database.append([condition[1:], current_node.freq])
                current_node = current_node.next_header_node

            conditional_tree = FPTree(conditional_database, self.min_support)
            if len(conditional_tree.header_table):
                conditional_tree.FPGrowth(freq_itemset, freq_itemsets)
