def filter_by_category(df, column_name, category):
    """
    Filters the DataFrame to include only rows where the specified category is found
    at any level of the hierarchy.

    Arguments:
    df -- DataFrame containing the data.
    column_name -- Name of the column containing the hierarchical data (slash-separated).
    category -- The category to filter on.

    Returns:
    filtered_df -- A DataFrame containing only the rows with the specified category.
    """
    # Filter rows where the category is in the slash-separated string
    filtered_df = df[df[column_name].str.contains(f"(^|/){category}(/|$)", regex=True)]
    return filtered_df