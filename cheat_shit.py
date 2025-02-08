def get_subcategories(df, column_name, category, depth=None):
    """
    Extracts subcategories under a specified category, with optional depth control.

    Arguments:
    df -- DataFrame containing the data.
    column_name -- Name of the column containing the hierarchical data (slash-separated).
    category -- The category to find subcategories for.
    depth -- Maximum depth of subcategories to retrieve (default: None, unlimited).

    Returns:
    subcategories -- A set of unique subcategories under the specified category.
    """
    subcategories = set()

    # Filter rows where the category is present
    filtered_df = df[df[column_name].str.contains(
        rf"(^{category}$)|(^|/){category}(/|$)",  # Improved RegEx
        regex=True, na=False
    )]

    # Extract subcategories from the filtered rows
    for hierarchy in filtered_df[column_name]:
        elements = hierarchy.split("/")
        
        # If the category is found, add all subsequent elements as subcategories
        if category in elements:
            index = elements.index(category)
            if depth is not None:
                subcategories.update(elements[index + 1 : index + 1 + depth])  # Limit depth
            else:
                subcategories.update(elements[index + 1:])  # Unlimited depth

    return subcategories