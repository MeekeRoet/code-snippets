import pytest
import pandas as pd
import numpy as np
import datetime
from ods_pythia.preprocessing.optimize import optimize_all
from pandas.testing import assert_series_equal


@pytest.fixture
def df_input():
    np.random.seed(16)

    ints = np.random.randint(low=-10, high=10, size=100)
    small_ints = ints
    medium_ints = ints * 1000
    large_ints = ints * 1_000_000
    huge_ints = ints * 1_000_000_000_000

    floats = np.random.random(100)
    small_floats = floats

    low_cardinal_object = list(map(str, np.random.choice(range(3), size=100)))
    high_cardinal_object = list(map(str, np.random.choice(range(100), size=100)))

    datetimes = np.random.choice(
        [
            (
                datetime.datetime(year=2019, month=9, day=8)
                + datetime.timedelta(days=i)
            ).strftime("%Y-%m-%d")
            for i in range(4)
        ],
        size=100,
    )

    df_input = pd.DataFrame(
        {
            "small_ints": small_ints,
            "medium_ints": medium_ints,
            "large_ints": large_ints,
            "huge_ints": huge_ints,
            "small_floats": small_floats,
            "low_cardinal_object": low_cardinal_object,
            "high_cardinal_object": high_cardinal_object,
            "datetimes": datetimes,
        }
    )
    return df_input


class TestOptimze:
    def test_normal_functionality(self, df_input):
        df_input = optimize_all(df_input, exclude=["datetimes"])

        index = [
            "small_ints",
            "medium_ints",
            "large_ints",
            "huge_ints",
            "small_floats",
            "low_cardinal_object",
            "high_cardinal_object",
            "datetimes",
        ]
        data = [
            "int8",
            "int16",
            "int32",
            "int64",
            "float32",
            "category",
            "object",
            "object",
        ]
        df_correct_output = pd.Series(data=data, index=index)

        assert_series_equal(df_input.dtypes, df_correct_output)