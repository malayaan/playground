def calculate_entity_comparison_df(df, question, dico, audit_team, audit_team_column="MainAuditTeam", business_line_column="MainBusinessLine"):
    """
    Calculates a comparison DataFrame for multiple audited entities answering a specific question.

    Arguments:
    df -- DataFrame containing the data.
    question -- The specific question to analyze.
    dico -- Dictionary where each key is a question, and each value is a tuple:
            (short_name, [list of possible answers in order from most negative to most positive]).
    audit_team -- The audit/inspection team to determine the scope of audited entities.
    audit_team_column -- Name of the column containing audit/inspection teams.
    business_line_column -- Name of the column containing the audited business lines.

    Returns:
    result_df -- A DataFrame containing entity, answer, percentage, and color gradient.
    """
    # Ensure the question exists in the dictionary
    if question not in dico:
        raise ValueError(f"Question '{question}' is not defined in the dictionary.")
    
    short_name, answer_list = dico[question]
    reversed_answer_list = answer_list[::-1]  # Reverse for gradient (green to red)

    # Extract audited entities directly from the audit_team_column
    df['audited_entity'] = df[audit_team_column].str.split("/", expand=True)[0]

    # Filter the DataFrame to only include rows for the specified audit team
    scoped_df = df[df['audited_entity'] == audit_team]

    if scoped_df.empty:
        print(f"No audited entities found for audit team '{audit_team}'.")
        return None

    # Prepare a DataFrame to store the results
    result_df = pd.DataFrame()

    # Group by business lines and calculate percentages
    for entity, group in scoped_df.groupby(business_line_column):
        # Filter for the specific question and answers
        filtered_group = group[(group['question'] == question) & (group['answer'].isin(reversed_answer_list))]
        
        if filtered_group.empty:
            print(f"No answers found for entity '{entity}' and question '{question}'.")
            continue

        # Count answers and normalize to percentages
        value_counts = filtered_group['answer'].value_counts()
        total_count = value_counts.sum()
        percentages = [((value_counts.get(answer, 0) / total_count) * 100) for answer in reversed_answer_list]

        # Append results for the current entity
        result_df = result_df.append(pd.DataFrame({
            'bar': [entity] * len(reversed_answer_list),
            'answer': reversed_answer_list,
            'percentage': percentages,
            'color': np.linspace(0, 1, len(reversed_answer_list))
        }), ignore_index=True)

    return result_df