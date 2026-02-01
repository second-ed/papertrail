def enum_keys(enum_dict: dict[int, str]) -> list[str]:
    """Multiply the values by the key amount."""
    return [i * a for i, a in enum_dict.items()]
