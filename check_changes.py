from get_ranges import get_ranges
import json


def get_functions(data: str, required: list) -> None:
    ranges = get_ranges(data)
    final_ranges = set([ ranges[i] for i in required])
    print(json.dumps(list(final_ranges)))
