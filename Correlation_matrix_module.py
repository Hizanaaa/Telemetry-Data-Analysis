from typing import Dict, List
import pandas as pd
import numpy as np


def compute_correlations(
    df: pd.DataFrame,
    threshold: float = 0.7
) -> Dict:
    
    #Validate inputs
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    if df.empty:
        raise ValueError("DataFrame cannot be empty")

    if not (0 <= threshold <= 1):
        raise ValueError("threshold must be between 0 and 1")

    # Keeping only the numeric columns for correlation analysis
    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.empty:
        raise ValueError("DataFrame contains no numeric columns")

    #Pearson Correlation Matrix: Measures linear relationships
    pearson_matrix = numeric_df.corr(method="pearson")

    # Spearman Correlation Matrix: Measures monotonicrelationships
    spearman_matrix = numeric_df.corr(method="spearman")

    #Find Interesting Pairs
    interesting = []

    columns = numeric_df.columns

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            col_a = columns[i]
            col_b = columns[j]

            pearson_value = pearson_matrix.loc[col_a, col_b]

            spearman_value = spearman_matrix.loc[col_a, col_b]

            #Interesting if either correlation exceeds threshold
            if (
                abs(pearson_value) >= threshold or
                abs(spearman_value) >= threshold
            ):

                interesting.append({
                    "a": str(col_a),
                    "b": str(col_b),
                    "pearson": round(float(pearson_value), 4),
                    "spearman": round(float(spearman_value), 4)
                })

    return {
        "pearson": pearson_matrix.round(4).to_dict(),
        "spearman": spearman_matrix.round(4).to_dict(),
        "interesting": interesting
    }