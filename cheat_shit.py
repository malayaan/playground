def calculate_result_df(df, entity_name, dico):
    """
    Calculates percentages for a specific entity based on the given dictionary (dico).
    Filters answers based on dico and normalizes percentages to 100%.

    Arguments:
    df -- DataFrame containing the survey responses.
    entity_name -- Name of the entity to analyze.
    dico -- Dictionary where each key is a question, and each value is a tuple:
            (short_name, [list of possible answers in order from most negative to most positive]).

    Returns:
    result_df -- A DataFrame containing bar, answer, percentage, and color gradient.
    """
    # Filter data for the specified entity
    entity_df = df[df['entity'] == entity_name]

    if entity_df.empty:
        print(f"No data found for the entity: {entity_name}")
        return None

    # Prepare a DataFrame to store percentages
    result_df = pd.DataFrame()

    # Process each question
    for question, (short_name, answer_list) in dico.items():
        # Reverse the answer list to invert the gradient
        reversed_answer_list = answer_list[::-1]

        # Filter data for the specific question
        question_df = entity_df[entity_df['question'] == question]

        if question_df.empty:
            print(f"No answers found for question: {question}")
            continue

        # Filter the answers based on the dictionary
        filtered_df = question_df[question_df['answer'].isin(reversed_answer_list)]

        # Count the answers and normalize to percentages
        value_counts = filtered_df['answer'].value_counts()
        total_count = value_counts.sum()
        percentages = [((value_counts.get(answer, 0) / total_count) * 100) for answer in reversed_answer_list]

        # Add to the result DataFrame
        result_df = result_df.append(pd.DataFrame({
            'bar': [short_name] * len(reversed_answer_list),  # Renamed column to 'bar'
            'answer': reversed_answer_list,
            'percentage': percentages,
            'color': np.linspace(0, 1, len(reversed_answer_list))  # Gradient from green to red
        }), ignore_index=True)

    return result_df