def map_value(value, from_min, from_max, to_min, to_max):
    """
    Map a value from one range to another.

    Args:
        value (float): The value to map.
        from_min (float): The minimum of the input range.
        from_max (float): The maximum of the input range.
        to_min (float): The minimum of the output range.
        to_max (float): The maximum of the output range.

    Returns:
        float: The mapped value within the output range.

    Example:
        mapped_value = map_value(5, 0, 10, 0, 100)  # Returns 50.0
    """
    # Ensure from_min and from_max are not equal to avoid division by zero
    if from_min == from_max:
        raise ValueError("from_min and from_max cannot be the same value.")

    # Normalize the value to a range of 0 to 1
    normalized_value = (value - from_min) / (from_max - from_min)

    # Scale the normalized value to the new range
    mapped_value = to_min + (normalized_value * (to_max - to_min))

    return mapped_value
