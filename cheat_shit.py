def plot_stacked_bar(result_df, title="Distribution of Answers", y_label="Percentage (%)"):
    """
    Plots a stacked bar chart based on the provided result DataFrame.

    Arguments:
    result_df -- DataFrame containing bar, answer, percentage, and color gradient.
    title -- Title of the chart (default: "Distribution of Answers").
    y_label -- Label for the y-axis (default: "Percentage (%)").
    """
    bars = result_df['bar'].unique()
    
    plt.figure(figsize=(10, 6))
    for i, bar in enumerate(bars):
        data = result_df[result_df['bar'] == bar]
        bottom = 0
        for _, row in data.iterrows():
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
    plt.xticks(range(len(bars)), bars, rotation=0, fontsize=10, ha='center')
    plt.yticks(range(0, 101, 10))
    plt.ylim(0, 100)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()
    plt.show()