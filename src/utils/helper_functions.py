import pygame as pg


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


def round_vec_2d(vec: pg.Vector2, decimal_places: int = 2):
    return pg.Vector2(
        round(vec[0], decimal_places),
        round(vec[1], decimal_places),
    )


def calculate_error_and_round(num: float, error_margin: float = 25):
    """
    Calculate the percentage error and check if it falls within the accepted error margin.

    Args:
        num (float): The number to evaluate.
        error_margin (float): The accepted error margin in percentage. For example, for +/-0.2, input 20. Defaults to 30.

    Returns:
        tuple or None: (rounded number as int, percentage error as int) if the error is within the margin, otherwise None.

    Examples:
        >>> calculate_error_and_round(17.2, 30)
        (17, 20.0)

        >>> calculate_error_and_round(17.2, 10)
        None

        >>> calculate_error_and_round(10.5, 50)
        (10, 50.0)

        >>> calculate_error_and_round(5.0, 0)
        (5, 0.0)
    """
    rounded_num = round(num)
    error = abs(num - rounded_num) * 100
    if error > error_margin:
        return None
    return rounded_num, error


def normalize_angle_90(angle):
    """
    Normalizes an angle to the nearest multiple of 90 within the range [0, 360).
    
    Args:
    - angle (float or int): The angle to normalize.
    
    Returns:
    - float: The normalized angle, rounded to a multiple of 90.
    """
    normalized = angle % 360  # Wrap the angle into the [0, 360) range
    if normalized == 360:
        normalized = 0  # Map 360 to 0
    return (round(normalized / 90) * 90) % 360


if __name__ == "__main__":

    print(calculate_error_and_round(17.4, 30))

    print(normalize_angle_90(355))  # Output: 0
    print(normalize_angle_90(370))  # Output: 0
    print(normalize_angle_90(10))  # Output: 0
    print(normalize_angle_90(200))  # Output: 180
    print(normalize_angle_90(290))  # Output: 270
    print(normalize_angle_90(-10))  # Output: 0
