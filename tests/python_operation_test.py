#  Copyright (c) 2024.  @Author: Aashish Mahajan
#

import pandas as pd
import pytest

from src.pandas_operation import calculate_mean_and_standard_deviation, filter_by_condition


@pytest.fixture
def sample_data():
    """Provides sample data for tests."""
    return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def test_calculate_mean_and_standard_deviation(sample_data):
    """Tests mean and standard deviation calculation."""
    mean, std = calculate_mean_and_standard_deviation(sample_data)
    assert mean.tolist() == [4, 5, 6]
    assert std.tolist() == [3.0, 3.0, 3.0]


def test_filter_by_condition():
    """Tests DataFrame filtering."""
    df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8]})
    filtered_df = filter_by_condition(df, "A", 2)
    filtered_df = filtered_df.reset_index(drop=True)
    expected_df = pd.DataFrame({"A": [3, 4], "B": [7, 8]})

    # Assert frame equality
    pd.testing.assert_frame_equal(filtered_df, expected_df)


def test_calculate_mean_and_standard_deviation_raises_error():
    """Tests error handling for invalid input."""
    with pytest.raises(ValueError):
        calculate_mean_and_standard_deviation("invalid_data")
