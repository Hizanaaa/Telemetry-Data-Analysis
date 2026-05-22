import numpy as np
import pandas as pd


def rolling_stats(values: np.ndarray, window: int, stats: list[str] = None) -> dict[str, list]:
 
    allowed_stats = {"mean", "std", "min", "max", "median"}

    #Default stats if not provided
    if stats is None:
        stats = ["mean", "std", "min", "max", "median"]
    
    if values is None:
        raise ValueError("values cannot be None")

    if not isinstance(window, int):
        raise TypeError("window must be an integer")

    if window <= 0:
        raise ValueError("window must be positive")

    if not isinstance(stats, (list, tuple)):
        raise TypeError("stats must be a list or tuple")

    invalid = [stat for stat in stats if stat not in allowed_stats]

    if invalid:
        raise ValueError(
            f"Unknown stat(s): {invalid}. "
            f"Allowed stats are: {sorted(allowed_stats)}"
        )

    try:
        values = np.asarray(values, dtype=float)
    except Exception:
        raise ValueError("values must contain numeric data")

    if values.ndim != 1:
        raise ValueError("values must be 1-dimensional")

    if np.any(np.isnan(values)):
        raise ValueError("values cannot contain NaN")

    if np.any(np.isinf(values)):
        raise ValueError("values cannot contain Inf")

    # Optional empty-array handling
    if len(values) == 0:
        return {stat: [] for stat in stats}
    
    series = pd.Series(values)
    rolling = series.rolling(window=window)
    result = {}

    for stat in stats:

        if stat == "mean":
            computed = rolling.mean()

        elif stat == "std":
            computed = rolling.std()

        elif stat == "min":
            computed = rolling.min()

        elif stat == "max":
            computed = rolling.max()

        elif stat == "median":
            computed = rolling.median()

        #Convert NaN -> None
        result[stat] = [
            None if pd.isna(v) else float(v)
            for v in computed.tolist()
        ]

    return result


if __name__ == "__main__":

    output = rolling_stats(np.arange(10), 3)
    from pprint import pprint
    pprint(output)