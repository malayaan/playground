import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analyze_easypoc_responses(df, entity_name, dico):
    """
    Analyzes EasyPOC survey responses for a specific entity and visualizes results with vertical bars.
    Uses the question short name from the dictionary for the x-axis labels.

    Arguments:
    df -- DataFrame containing EasyPOC survey responses.
    entity_name -- Name of the entity to analyze.
    dico -- Dictionary with questions of interest as keys. Each value is a tuple:
            (short_name, [list of possible answers in order from most negative to most positive]).

    Returns:
    A vertical bar chart visualizing response distributions and a DataFrame of percentages.
    """
    # Filter the DataFrame for the specified entity
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
            'question': [short_name] * len(reversed_answer_list),
            'answer': reversed_answer_list,
            'percentage': percentages,
            'color': np.linspace(0, 1, len(reversed_answer_list))  # Gradient from green to red
        }), ignore_index=True)

    # Create a vertical bar chart
    questions = result_df['question'].unique()
    plt.figure(figsize=(10, 6))
    for i, question in enumerate(questions):
        data = result_df[result_df['question'] == question]
        bottom = 0
        for _, row in data.iterrows():
            plt.bar(
                x=i, 
                height=row['percentage'], 
                bottom=bottom, 
                color=plt.cm.RdYlGn(row['color']),  # Adjusted gradient
                edgecolor='black', 
                width=0.8
            )
            bottom += row['percentage']  # Increment the bottom for stacking

    # Set x-axis and y-axis labels
    plt.xticks(range(len(questions)), questions, rotation=45, ha='right')
    plt.yticks(range(0, 101, 10))
    plt.ylim(0, 100)
    plt.ylabel('Percentage (%)')
    plt.title(f'Distribution of Answers for Entity: {entity_name}')
    plt.tight_layout()
    plt.show()

    return result_df