import numpy as np

def detect_changepoints(values: np.ndarray,penalty: float = 10.0) -> list[int]:
    
    #Input Validation
    if values is None:
        raise ValueError("values cannot be None")

    try:
        values = np.asarray(values, dtype=float)
    except Exception:
        raise ValueError("values must contain numeric data")

    if values.ndim != 1:
        raise ValueError("values must be 1-dimensional")

    if len(values) == 0:
        return []

    if np.any(np.isnan(values)):
        raise ValueError("values cannot contain NaN")

    if np.any(np.isinf(values)):
        raise ValueError("values cannot contain Inf")

    if penalty <= 0:
        raise ValueError("penalty must be positive")

    #Constant signal, no change-points
    if np.all(values == values[0]):
        return []

    changepoints = []

    #Segment Score Function
    def segment_cost(segment: np.ndarray) -> float:
        """
        Cost = variance * length
        Lower cost means tighter/more consistent segment.
        """
        if len(segment) <= 1:
            return 0.0

        return np.var(segment) * len(segment)

    #Binary Segmentation
    def binary_segment(start: int, end: int):

        segment = values[start:end]

        #Too small to split meaningfully
        if len(segment) < 6:
            return

        full_cost = segment_cost(segment)

        best_improvement = 0.0
        best_split = None

        #Avoiding tiny splits near edges
        for split in range(start + 3, end - 3):

            left = values[start:split]
            right = values[split:end]

            split_cost = (
                segment_cost(left) +
                segment_cost(right)
            )

            improvement = full_cost - split_cost

            if improvement > best_improvement:
                best_improvement = improvement
                best_split = split

        #Accepts split only if improvement exceeds penalty
        if best_split is not None and best_improvement > penalty:

            changepoints.append(best_split)

            #Recurse on left and right halves
            binary_segment(start, best_split)
            binary_segment(best_split, end)

    #Recursive segmentation
    binary_segment(0, len(values))

    #Merging nearby change-points (within 3 indices)
    changepoints.sort()

    merged = []

    for cp in changepoints:

        if not merged:
            merged.append(cp)

        elif cp - merged[-1] >= 3:
            merged.append(cp)

    return merged


if __name__ == "__main__":

    test_values = np.array([1] * 50 + [10] * 50)

    cps = detect_changepoints(test_values)

    print("Detected change-points:", cps)