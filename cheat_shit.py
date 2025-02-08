def filter_by_category(df, column_name, category):
    """
    Filters the DataFrame to include only rows where the specified category is found
    at any level of the hierarchy, while handling empty or missing values robustly.

    Arguments:
    df -- DataFrame containing the data.
    column_name -- Name of the column containing the hierarchical data (slash-separated).
    category -- The category to filter on.

    Returns:
    filtered_df -- A DataFrame containing only the rows with the specified category.
    """
    # Ensure the column exists and is not empty
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")

    # Filter out rows where the column is empty or contains NaN
    valid_df = df[df[column_name].notna() & (df[column_name].str.strip() != "")]
    
    # Apply the category filtering
    filtered_df = valid_df[valid_df[column_name].str.contains(f"(^|/){category}(/|$)", regex=True)]
    
    return filtered_df