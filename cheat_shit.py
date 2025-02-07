def plot_stacked_bar(result_df, title="Distribution of Answers", y_label="Percentage (%)"):
    """
    Plots a cleaner and improved stacked bar chart based on the provided result DataFrame.

    Arguments:
    result_df -- DataFrame containing bar, answer, percentage, and color gradient.
    title -- Title of the chart (default: "Distribution of Answers").
    y_label -- Label for the y-axis (default: "Percentage (%)").
    """
    bars = result_df['bar'].unique()
    
    # Initialize the figure with a custom size
    plt.figure(figsize=(10, 6))
    
    # Draw the bars
    for i, bar in enumerate(bars):
        data = result_df[result_df['bar'] == bar]
        bottom = 0
        for _, row in data.iterrows():
            plt.bar(
                x=i, 
                height=row['percentage'], 
                bottom=bottom, 
                color=plt.cm.RdYlGn(row['color']), 
                width=0.8
            )
            bottom += row['percentage']  # Increment the bottom for stacking

    # Customize the x-axis
    plt.xticks(
        range(len(bars)), 
        bars, 
        rotation=45,  # Rotate x-axis labels for better readability
        fontsize=10, 
        ha='right'
    )
    
    # Customize the y-axis
    plt.yticks([20, 40, 60, 80, 100], labels=["20%", "40%", "60%", "80%", "100%"], fontsize=10)
    plt.ylim(0, 100)

    # Add horizontal grid lines for better readability
    plt.gca().yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)
    plt.gca().set_axisbelow(True)  # Place grid lines below the bars

    # Remove the black borders around the chart
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    # Add axis labels and title
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=14, pad=15)

    # Adjust layout to prevent overlapping elements
    plt.tight_layout()
    plt.show()