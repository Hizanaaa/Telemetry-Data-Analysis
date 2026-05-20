from datetime import datetime, timedelta, timezone
from typing import Dict
import numpy as np


def predict_crossing(
    timestamps: np.ndarray,
    values: np.ndarray,
    target: float,
    lookback: int = 100
) -> Dict:
    
    if len(timestamps) != len(values):
        raise ValueError("timestamps and values must have same length")

    if len(timestamps) < 2:
        raise ValueError("At least 2 samples are required")

    #Keeping only the most recent 'lookback' samples for linear regression
    timestamps = timestamps[-lookback:]
    values = values[-lookback:]

    #normalizing timestamps to improve numerical stability
    base_timestamp = timestamps[0]
    normalized_timestamps = timestamps - base_timestamp

    #Linear Regression 
    slope, intercept = np.polyfit(
        normalized_timestamps,
        values,
        1
    )

    #Predicted values
    predicted_values = slope * normalized_timestamps + intercept

    #Calculating Residuals 
    ss_res = np.sum((values - predicted_values) ** 2)

    #Total sum of squares
    ss_tot = np.sum((values - np.mean(values)) ** 2)

    #Calculating R-squared
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 1.0

    #prediction variables
    predicted_crossing_at = None
    time_remaining_seconds = None



    if slope != 0:
        crossing_time_normalized = (target - intercept) / slope

        # Convert normalized time back to real UNIX timestamp
        crossing_timestamp = base_timestamp + crossing_time_normalized

        current_time = timestamps[-1]

        #Only future crossings are useful
        if crossing_timestamp > current_time:

            crossing_datetime = datetime.fromtimestamp(
                crossing_timestamp,
                timezone.utc
            )

            predicted_crossing_at = (
                crossing_datetime.isoformat()
            )

            time_remaining_seconds = int(
                crossing_timestamp - current_time
            )

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r_squared": float(r_squared),
        "predicted_crossing_at": predicted_crossing_at,
        "time_remaining_seconds": time_remaining_seconds,
    }