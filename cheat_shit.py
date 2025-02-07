def plot_stacked_bar(result_df, title="Distribution of Answers"):
    """
    Plots a cleaner and improved stacked bar chart with auto-wrapping for x-axis labels
    and without a percentage label on the y-axis.

    Arguments:
    result_df -- DataFrame containing bar, answer, percentage, and color gradient.
    title -- Title of the chart (default: "Distribution of Answers").
    """
    def wrap_label(label, max_words=2):
        """
        Wraps a label to add line breaks every `max_words` words.

        Arguments:
        label -- The original label (string).
        max_words -- Maximum number of words per line.

        Returns:
        A string with line breaks for wrapping.
        """
        words = label.split()
        return '\n'.join([' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)])
    
    # Apply the wrapping function to x-axis labels
    bars = result_df['bar'].unique()
    wrapped_labels = [wrap_label(bar, max_words=2) for bar in bars]
    
    # Initialize the figure
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
        wrapped_labels,  # Use the wrapped labels
        rotation=0,  # No need for rotation after wrapping
        fontsize=10, 
        ha='center'
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

    # Remove the y-axis label
    plt.gca().set_ylabel(None)

    # Add title
    plt.title(title, fontsize=14, pad=15)

    # Adjust layout to prevent overlapping elements
    plt.tight_layout()
    plt.show()