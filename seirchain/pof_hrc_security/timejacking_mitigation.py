import numpy as np

def is_timestamp_valid(new_triad, parent_triads):
    """
    Validates the timestamp of a new triad based on the median of parent timestamps.
    """
    if len(parent_triads) < 11:
        # Not enough parents to validate, so we assume it's valid for now
        return True

    parent_timestamps = [triad.timestamp for triad in parent_triads[-11:]]
    median_timestamp = np.median(parent_timestamps)

    return new_triad.timestamp > median_timestamp
