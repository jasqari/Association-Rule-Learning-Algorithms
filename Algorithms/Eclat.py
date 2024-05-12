def eclat(vertical_db, prev_condition, freq_items):
    while len(vertical_db):
        item, tid_set = vertical_db.pop()
        item_support = len(tid_set)
        if item_support >= 2:
            freq_items[frozenset(prev_condition + [item])] = item_support
            new_condition = []
            for new_item, new_tid_set in vertical_db:
                intersection = set.intersection(tid_set, new_tid_set)
                intersection_support = len(intersection)
                if intersection_support >= 2:
                    new_condition.append((new_item, new_tid_set))
            eclat(
                sorted(new_condition, key=lambda x: len(x[1]), reverse=True),
                (prev_condition + [item]),
                freq_items,
            )
