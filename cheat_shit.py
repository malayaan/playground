import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_easypoc_responses(df, entity_name, dico):
    """
    Analyzes EasyPOC survey responses for a specific entity, focusing only on questions defined in the dictionary.
    Outputs a DataFrame with percentages and a gradient-colored heatmap.

    Arguments:
    df -- DataFrame containing the EasyPOC survey responses.
    entity_name -- Name of the entity to analyze.
    dico -- Dictionary with questions of interest as keys and possible answers (from most positive to most negative) as values.

    Returns:
    A DataFrame containing percentages for each response and a heatmap visualization.
    """
    # Filter data for the specified entity
    entity_df = df[df['entity'] == entity_name]

    if entity_df.empty:
        print(f"No data found for the entity: {entity_name}")
        return None

    # Prepare a results DataFrame
    result_df = pd.DataFrame(columns=['Question', 'Response', 'Percentage'])

    # Calculate percentages for each question of interest
    for question, response_list in dico.items():
        if question in df.columns:
            value_counts = entity_df[question].value_counts(normalize=True) * 100
            for response in response_list:
                percentage = value_counts.get(response, 0)
                result_df = result_df.append({
                    'Question': question,
                    'Response': response,
                    'Percentage': percentage
                }, ignore_index=True)

    # Pivot the data for better visualization
    pivot_df = result_df.pivot(index='Question', columns='Response', values='Percentage').fillna(0)

    # Reorder columns based on the response order in the dictionary
    pivot_df = pivot_df[[response for question in dico.keys() for response in dico[question] if response in pivot_df.columns]]

    # Plot a heatmap to visualize percentages with a gradient
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_df, annot=True, fmt=".1f", cmap="RdYlGn", cbar_kws={'label': 'Percentage (%)'}, linewidths=0.5)
    plt.title(f"Distribution of Responses for Entity: {entity_name}")
    plt.xlabel("Responses")
    plt.ylabel("Questions")
    plt.tight_layout()
    plt.show()

    return result_df