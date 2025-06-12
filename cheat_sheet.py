# Step 6: Compute phases on rolling std
phases = pd.DataFrame(index=rolling_std.index)

for sector in rolling_std.columns:
    signal = rolling_std[sector].values
    analytic_signal = hilbert(signal)
    phases[sector] = np.unwrap(np.angle(analytic_signal))  # Phase in radians, unwrapped

# Option: re-wrap to [-pi, pi] for heatmap clarity
phases_wrapped = (phases + np.pi) % (2 * np.pi) - np.pi

# Step 7: Plot phase heatmap
plt.figure(figsize=(12, 8))
ax = sns.heatmap(phases_wrapped.T, cmap='twilight_shifted', center=0,
                 cbar_kws={'label': 'Phase (radians)', 'ticks': [-np.pi, -np.pi/2, 0, np.pi/2, np.pi]})

# Clean x-axis
ax.set_xticklabels(phases_wrapped.index[::30].strftime('%Y-%m-%d'), rotation=45, ha='right', fontsize=10)

# Titles
plt.title("Hilbert Phase Heatmap (Rolling Std Stress Cycles)", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Sectors", fontsize=12)
plt.tight_layout()
plt.show()