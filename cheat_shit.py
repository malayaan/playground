def get_business_line_by_audit_team(df, audit_team_column, business_line_column, audit_team):
    """
    Retrieves the list of second elements (or unique elements if only one exists) 
    in the "Main Business Line" column for a given audit/inspection team.

    Arguments:
    df -- DataFrame containing the data.
    audit_team_column -- Name of the column containing the audit/inspection teams.
    business_line_column -- Name of the column containing the business lines.
    audit_team -- The audit/inspection team to filter on.

    Returns:
    business_lines -- A set of unique second-level (or unique) elements in the business line hierarchy.
    """
    business_lines = set()
    
    # Filter rows where the audit team matches
    filtered_df = df[df[audit_team_column].str.contains(
        rf"(^{audit_team}$)|(^|/){audit_team}(/|$)",  # Robust regex for audit team matching
        regex=True, na=False
    )]

    # Extract and process the business line elements
    for business_line in filtered_df[business_line_column]:
        if pd.isna(business_line) or business_line.strip() == "":
            # Skip empty or NaN values
            continue

        # Split the business line into parts
        elements = business_line.split("/")
        
        if len(elements) == 1:
            # If only one element, add it as is
            business_lines.add(elements[0].strip())
        elif len(elements) > 1:
            # If multiple elements, add the second element
            business_lines.add(elements[1].strip())

    return business_lines