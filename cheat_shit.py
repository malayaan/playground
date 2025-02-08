def calculate_entity_comparison_df(df, audit_team_column, business_line_column, question, dico, audit_team):
    """
    Calculates a comparison DataFrame for multiple audited entities answering a specific question.

    Arguments:
    df -- DataFrame containing the data.
    audit_team_column -- Name of the column containing audit/inspection teams.
    business_line_column -- Name of the column containing the audited business lines.
    question -- The specific question to analyze.
    dico -- Dictionary where each key is a question, and each value is a tuple:
            (short_name, [list of possible answers in order from most negative to most positive]).
    audit_team -- The audit/inspection team to determine the scope of audited entities.

    Returns:
    result_df -- A DataFrame containing entity, answer, percentage, and color gradient.
    """
    # Ensure the question exists in the dictionary
    if question not in dico:
        raise ValueError(f"Question '{question}' is not defined in the dictionary.")
    
    short_name, answer_list = dico[question]
    reversed_answer_list = answer_list[::-1]  # Reverse for gradient (green to red)

    # Get the list of entities audited by the given audit team
    audited_entities = get_business_line_by_audit_team(df, audit_team_column, business_line_column, audit_team)

    if not audited_entities:
        print(f"No audited entities found for audit team '{audit_team}'.")
        return None

    # Prepare a DataFrame to store the results
    result_df = pd.DataFrame()

    # Process each audited entity
    for entity in audited_entities:
        # Filter the DataFrame for the current entity and question
        entity_df = df[(df[business_line_column] == entity) & (df['question'] == question)]

        if entity_df.empty:
            print(f"No answers found for entity '{entity}' and question '{question}'.")
            continue

        # Filter answers based on the dictionary
        filtered_df = entity_df[entity_df['answer'].isin(reversed_answer_list)]

        # Count answers and normalize to percentages
        value_counts = filtered_df['answer'].value_counts()
        total_count = value_counts.sum()
        percentages = [((value_counts.get(answer, 0) / total_count) * 100) for answer in reversed_answer_list]

        # Add to the result DataFrame
        result_df = result_df.append(pd.DataFrame({
            'bar': [entity] * len(reversed_answer_list),  # Use entity names in 'bar' column
            'answer': reversed_answer_list,
            'percentage': percentages,
            'color': np.linspace(0, 1, len(reversed_answer_list))  # Gradient from green to red
        }), ignore_index=True)

    return result_df