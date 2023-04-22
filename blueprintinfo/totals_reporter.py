"""
Get item totals for a given blueprint.
"""

from collections import defaultdict

def count_items_and_report(bp_dict:dict) -> list:
    """
    Count the items in a blueprint & report, showing highest-to-lowest counts.
    """
    totals = count_items(bp_dict)
    results = []

    for items in totals.items():
        results.append(items)

    return sorted(results, key=lambda item:item[1], reverse=True)

def count_items(bp_dict):
    totals = defaultdict(int)

    for item in bp_dict['blueprint']['entities']:
        totals[item['name']] += 1

    return totals
