import numpy as np

def find_lag(a: np.ndarray,b: np.ndarray,max_lag: int = 50) -> dict:
    #Input validation
    if a is None or b is None:
        raise ValueError("Input arrays cannot be None")

    try:
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
    except Exception:
        raise ValueError("Inputs must contain numeric data")

    if a.ndim != 1 or b.ndim != 1:
        raise ValueError("Inputs must be 1-dimensional")

    if len(a) != len(b):
        raise ValueError("Input arrays must have equal length")

    if len(a) == 0:
        raise ValueError("Input arrays cannot be empty")

    if np.any(np.isnan(a)) or np.any(np.isnan(b)):
        raise ValueError("Inputs cannot contain NaN")

    if np.any(np.isinf(a)) or np.any(np.isinf(b)):
        raise ValueError("Inputs cannot contain Inf")

    if not isinstance(max_lag, int):
        raise TypeError("max_lag must be an integer")

    if max_lag < 0:
        raise ValueError("max_lag must be non-negative")

    n = len(a)

    min_overlap = 10

    lag_curve = []

    best_lag = 0
    best_corr = 0.0

    #Lag sweep from -max_lag to +max_lag
    for lag in range(-max_lag, max_lag + 1):

        #b leads a
        if lag < 0:
            overlap_a = a[-lag:]
            overlap_b = b[:n + lag]

        #b follows a
        elif lag > 0:
            overlap_a = a[:n - lag]
            overlap_b = b[lag:]

        #no lag
        else:
            overlap_a = a
            overlap_b = b

        if len(overlap_a) < min_overlap:
            corr = 0.0

        #Constant overlap segments -> correlation undefined
        elif np.std(overlap_a) == 0 or np.std(overlap_b) == 0:
            corr = 0.0

        else:

            corr = np.corrcoef(overlap_a, overlap_b)[0, 1]

            # Numerical safety
            if np.isnan(corr):
                corr = 0.0

        lag_curve.append(float(corr))

        if abs(corr) > abs(best_corr):

            best_corr = corr
            best_lag = lag

    return {
        "best_lag": best_lag,
        "correlation": float(best_corr),
        "lag_curve": lag_curve
    }


if __name__ == "__main__":

    np.random.seed(42)
    a = np.random.randn(200)

    shift = 5

    #shift right by 5
    b = np.concatenate([
        np.zeros(shift),
        a[:-shift]
    ])

    result = find_lag(a, b, max_lag=20)
    print("Best lag:", result["best_lag"])
    print("Correlation:", result["correlation"])
    
    #Shift left by 5
    C = np.concatenate([
    a[shift:],
    np.zeros(shift)
    ])
    result = find_lag(a, C, max_lag=20)

    print("Best lag:", result["best_lag"])
    print("Correlation:", result["correlation"])