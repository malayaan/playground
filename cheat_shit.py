def extract_hierarchy(df, column_name):
    """
    Extracts a hierarchy mapping from a DataFrame column, creating a dictionary where:
    - The keys are the first elements in the slash-separated string.
    - The values are lists of second elements in the slash-separated string.

    Arguments:
    df -- DataFrame containing the data.
    column_name -- Name of the column containing the slash-separated strings.

    Returns:
    hierarchy_dict -- A dictionary where keys are the first elements, and values are lists of second elements.
    """
    hierarchy_dict = {}

    for row in df[column_name]:
        # Split the row by slashes
        elements = row.split("/")
        
        if len(elements) > 1:  # Ensure there are at least two elements
            key = elements[0].strip()  # The first element (key), remove extra spaces
            value = elements[1].strip()  # The second element (value), remove extra spaces
            
            # Add the value to the corresponding key in the dictionary
            if key not in hierarchy_dict:
                hierarchy_dict[key] = []
            hierarchy_dict[key].append(value)

    # Remove duplicates in the lists for each key
    for key in hierarchy_dict:
        hierarchy_dict[key] = list(set(hierarchy_dict[key]))

    return hierarchy_dict