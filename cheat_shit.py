def calculate_entity_comparison_df(df, entity_col, entities, question, dico):
    """
    Calculates a comparison DataFrame for multiple entities answering a specific question.

    Arguments:
    df -- DataFrame containing the survey responses.
    entity_col -- Name of the column containing entity names.
    entities -- List of entities to include in the comparison.
    question -- The specific question to analyze.
    dico -- Dictionary where each key is a question, and each value is a tuple:
            (short_name, [list of possible answers in order from most negative to most positive]).

    Returns:
    result_df -- A DataFrame containing entity, answer, percentage, and color gradient.
    """
    # Ensure the question exists in the dictionary
    if question not in dico:
        raise ValueError(f"Question '{question}' is not defined in the dictionary.")
    
    short_name, answer_list = dico[question]
    reversed_answer_list = answer_list[::-1]  # Reverse for gradient (green to red)

    # Prepare a DataFrame to store the results
    result_df = pd.DataFrame()

    # Process each entity
    for entity in entities:
        # Filter the DataFrame for the current entity and question
        entity_df = df[(df[entity_col] == entity) & (df['question'] == question)]

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
            'bar': [entity] * len(reversed_answer_list),  # Entity names go into 'bar' for plotting
            'answer': reversed_answer_list,
            'percentage': percentages,
            'color': np.linspace(0, 1, len(reversed_answer_list))  # Gradient from green to red
        }), ignore_index=True)

    return result_df