def get_subcategories(df, column_name, category):
    """
    Extracts all subcategories under a specified category, regardless of hierarchy depth.

    Arguments:
    df -- DataFrame containing the data.
    column_name -- Name of the column containing the hierarchical data (slash-separated).
    category -- The category to find subcategories for.

    Returns:
    subcategories -- A set of unique subcategories under the specified category.
    """
    subcategories = set()

    # Filter rows where the category is present
    filtered_df = df[df[column_name].str.contains(f"(^|/){category}(/|$)", regex=True)]

    # Extract subcategories from the filtered rows
    for hierarchy in filtered_df[column_name]:
        elements = hierarchy.split("/")
        
        # If the category is found, add all subsequent elements as subcategories
        if category in elements:
            index = elements.index(category)
            subcategories.update(elements[index + 1:])

    return subcategories