import pytest
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from seirchain.structures.triad import Triad, is_timestamp_valid

@pytest.fixture
def parent_timestamps():
    return [int(time.time()) - i for i in range(20, 0, -1)][::-1]

def test_valid_timestamp(parent_timestamps):
    timestamp = int(time.time())
    triad = Triad([], "parent_hash", "pof_data", timestamp, parent_timestamps)
    assert triad.timestamp == timestamp

def test_invalid_timestamp(parent_timestamps):
    timestamp = parent_timestamps[-5]
    print(f"Timestamp: {timestamp}")
    print(f"Parent timestamps: {parent_timestamps}")
    with pytest.raises(ValueError, match="Invalid timestamp"):
        Triad([], "parent_hash", "pof_data", timestamp, parent_timestamps)

def test_median_calculation(parent_timestamps):
    assert is_timestamp_valid(int(time.time()), parent_timestamps)
    assert not is_timestamp_valid(parent_timestamps[-6], parent_timestamps)

def test_less_than_11_parents(parent_timestamps):
    parent_timestamps = parent_timestamps[:5]
    timestamp = int(time.time())
    triad = Triad([], "parent_hash", "pof_data", timestamp, parent_timestamps)
    assert triad.timestamp == timestamp
