import numpy as np

def downsample_lttb(x: list, y: list, target_points: int) -> tuple[list, list]:

    #Validate the inputs
    if x is None or y is None:
        raise ValueError("x and y cannot be None")

    if not isinstance(target_points, int):
        raise TypeError("target_points must be an integer")

    if target_points <= 0:
        raise ValueError("target_points must be positive")

    try:
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
    except Exception:
        raise ValueError("x and y must contain numeric values")

    if len(x) != len(y):
        raise ValueError("x and y must have the same length")

    if len(x) == 0:
        return [], []

    if np.any(np.isnan(x)) or np.any(np.isnan(y)):
        raise ValueError("x and y cannot contain NaN")

    if np.any(np.isinf(x)) or np.any(np.isinf(y)):
        raise ValueError("x and y cannot contain Inf")

    #Dataset size 
    n = len(x)

    #Handling edge cases
    if n == 0:
        return [], []

    if target_points >= n:
        return list(x), list(y)

    if target_points < 3:
        return [x[0], x[-1]], [y[0], y[-1]]

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    #Output Storage
    sampled_x = [x[0]]
    sampled_y = [y[0]]

    #Bucket size calculation
    bucket_size = (n - 2) / (target_points - 2)

    #index of selected point(first point is already selected)
    a = 0


    for i in range(target_points - 2):

        #Current bucket range
        start = int(np.floor(i * bucket_size)) + 1
        end = int(np.floor((i + 1) * bucket_size)) + 1

        if end >= n:
            end = n - 1

        # Next bucket range for averaging
        next_start = int(np.floor((i + 1) * bucket_size)) + 1
        next_end = int(np.floor((i + 2) * bucket_size)) + 1

        if next_end >= n:
            next_end = n

        avg_x = np.mean(x[next_start:next_end])
        avg_y = np.mean(y[next_start:next_end])

        ax = x[a]
        ay = y[a]

        bucket_x = x[start:end]
        bucket_y = y[start:end]

        # Triangle areas
        areas = 0.5 * np.abs(
            (ax - avg_x) * (bucket_y - ay)
            - (ax - bucket_x) * (avg_y - ay)
        )

        max_index = np.argmax(areas)

        selected_index = start + max_index

        sampled_x.append(x[selected_index])
        sampled_y.append(y[selected_index])

        a = selected_index

    #keeping the last point 
    sampled_x.append(x[-1])
    sampled_y.append(y[-1])

    return sampled_x, sampled_y

if __name__ == "__main__":

    x = np.linspace(0, 100, 5000)
    y = np.sin(x)

    spike_index = 2500
    y[spike_index] = 10

    down_x, down_y = downsample_lttb(x.tolist(), y.tolist(), 100)

    spike_x = x[spike_index]

    print(f"Original points: {len(x)}")
    print(f"Downsampled points: {len(down_x)}")