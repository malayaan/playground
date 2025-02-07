import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analyze_easypoc_responses(df, entity_name, dico):
    """
    Analyzes EasyPOC survey responses for a specific entity and visualizes results with vertical bars.
    Each question has a continuous bar segmented by percentage categories, with a gradient from red to green.

    Arguments:
    df -- DataFrame containing EasyPOC survey responses.
    entity_name -- Name of the entity to analyze.
    dico -- Dictionary with questions of interest as keys and possible responses (ordered from most negative to most positive).

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
    for question, response_list in dico.items():
        # Filter data for the specific question
        question_df = entity_df[entity_df['question'] == question]

        if question_df.empty:
            print(f"No responses found for question: {question}")
            continue

        # Count the responses and normalize to percentages
        value_counts = question_df['response'].value_counts(normalize=True) * 100
        percentages = [value_counts.get(response, 0) for response in response_list]

        # Add to the result DataFrame
        result_df = result_df.append(pd.DataFrame({
            'question': [question] * len(response_list),
            'response': response_list,
            'percentage': percentages,
            'color': np.linspace(0, 1, len(response_list))  # Gradient from red to green
        }), ignore_index=True)

    # Pivot for visualization
    questions = result_df['question'].unique()

    # Create a vertical bar chart
    plt.figure(figsize=(10, 6))
    for i, question in enumerate(questions):
        data = result_df[result_df['question'] == question]
        bottom = 0
        for j, row in data.iterrows():
            plt.bar(
                x=i, 
                height=row['percentage'], 
                bottom=bottom, 
                color=plt.cm.RdYlGn(row['color']), 
                edgecolor='black', 
                width=0.8
            )
            bottom += row['percentage']  # Increment the bottom for stacking

    # Set x-axis and y-axis labels
    plt.xticks(range(len(questions)), questions, rotation=45, ha='right')
    plt.yticks(range(0, 101, 10))
    plt.ylim(0, 100)
    plt.ylabel('Percentage (%)')
    plt.title(f'Distribution of Responses for Entity: {entity_name}')
    plt.tight_layout()
    plt.show()

    return result_df