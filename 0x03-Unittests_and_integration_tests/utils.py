from typing import Mapping, Sequence, Any

def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access values in a nested map using a sequence of keys.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map
