import re
import pandas as pd


def clean_text_column(df, column_name):
    """
    Cleans a text column in a DataFrame by:
    1. Replacing backslashes and slashes
    2. Removing broken words with hyphen + newline
    3. Removing repeated section headers (like 'X v Y judgment')
    4. Normalizing multiple spaces and newlines
    5. Removing numeric lines (page numbers, document IDs)
    6. Stripping leading/trailing whitespace

    Parameters:
    df : pd.DataFrame
        The dataframe containing the text column
    column_name : str
        The name of the column to clean

    Returns:
    pd.Series
        The cleaned text column
    """

    cleaned = df[column_name].astype(str)  # ensure all entries are strings

    # Step 1: Replace backslashes and slashes
    cleaned = cleaned.str.replace('\\', ' ', regex=False).str.replace('/', ' ', regex=False)

    # Step 2: Remove broken words with hyphen + newline
    cleaned = cleaned.str.replace(r'-\s*\n\s*', '', regex=True)

    # Step 3: Remove repeated section headers (example: "X v Y judgment")
    cleaned = cleaned.str.replace(r'\b[a-z]+\s+v\s+[a-z]+\s+judgment\b', '', regex=True, flags=re.IGNORECASE)

    # Step 4: Replace multiple spaces and newlines with a single space
    cleaned = cleaned.apply(lambda t: re.sub(r'\s+', ' ', t))

    # Step 5: Remove numeric lines (page numbers, document IDs)
    cleaned = cleaned.apply(lambda t: re.sub(r'^\s*\d+\s*$', '', t, flags=re.MULTILINE))

    # Step 6: Strip leading/trailing whitespace
    cleaned = cleaned.apply(lambda t: re.sub(r'\s+', ' ', t).strip())

    return cleaned
