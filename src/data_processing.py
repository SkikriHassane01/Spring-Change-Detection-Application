
import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize DataFrame columns:
      - Convert all-X columns to 0/1 integers
      - Strip and lowercase text columns
      - Fill other NaNs with zeros

    Args:
        df: Input DataFrame to clean.

    Returns:
        A new DataFrame with cleaned data.
    """
    df = df.copy()
    for col in df.columns:
        s = df[col]
        # normalize checkbox columns (all 'X' → 1, else 0)
        if s.dropna().astype(str).str.upper().isin({'X'}).all():
            df[col] = s.astype(str).str.upper().eq('X').astype(int)
        # strip whitespace & lowercase text
        elif pd.api.types.is_object_dtype(s):
            df[col] = s.fillna('').astype(str).str.strip().str.lower()
        # fill other missing values with 0
        else:
            df[col] = s.fillna(0)
    return df