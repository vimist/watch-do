"""A variety of helper functions that Watch Do makes use of.
"""

def diff_set(set_a, set_b):
    """Get the difference between two sets.

    Compare two sets and get the items that aren't in both.

    Parameters:
        set_a (set): The first set of values to compare.
        set_a (set): The second set of values to compare.

    Returns:
        set: A set containing the items that aren't in both set_a and set_b.
    """
    in_list_a_but_not_list_b = set_a - set_b
    in_list_b_but_not_list_a = set_b - set_a

    return in_list_b_but_not_list_a.union(in_list_a_but_not_list_b)
