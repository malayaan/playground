import pandas as pd
import matplotlib.pyplot as plt

# Load the data (extracted manually from the graph)
data = {
    "Manufacturer": [
        "BMW", "Ford", "Hyundai", "Kia", "Mercedes-Benz", 
        "Renault-Nissan-Mitsubishi", "Stellantis", "Toyota", 
        "Volkswagen", "Volvo", "Fleet average"
    ],
    "2023_CO2": [104, 94, 94, 94, 109, 111, 105, 109, 120, 70, 94],
    "2025_Target": [119, 119, 104, 104, 109, 109, 105, 105, 120, 90, 107],
    "Reduction": [-13, -21, -10, -10, 0, -2, 0, -4, -21, -30, -12]  # Expressed as %
}

df = pd.DataFrame(data)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(df["Manufacturer"], df["2025_Target"], label='2025 Target', color='#1f77b4')
bars2 = ax.bar(df["Manufacturer"], df["2023_CO2"], label='2023 CO₂', color='#ff7f0e')

# Draw labels and arrows for the reductions
for idx, (x, y2023, y2025, reduction) in enumerate(zip(df["Manufacturer"], df["2023_CO2"], df["2025_Target"], df["Reduction"])):
    ax.text(idx, max(y2023, y2025) + 2, f'{y2025}', ha='center', va='bottom', fontsize=9)
    ax.text(idx, y2023 - 5, f'{y2023}', ha='center', va='top', fontsize=9)
    ax.annotate(f'{reduction}%', xy=(idx, y2025), xytext=(idx, y2023),
                arrowprops=dict(facecolor='gray', arrowstyle='->'),
                ha='center', fontsize=8)

# Aesthetics
ax.set_ylabel('Estimated CO₂ performance (g/km)')
ax.set_title("2025 Manufacturer CO₂ targets versus 2023 fleet performance")
ax.legend()

plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()