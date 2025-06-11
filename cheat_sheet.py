# Rolling z-score 30 jours
df_merged['z_csd'] = (df_merged['std_cross_sector'] - df_merged['std_cross_sector'].rolling(30).mean()) / df_merged['std_cross_sector'].rolling(30).std()
df_merged['z_vstoxx'] = (df_merged['Indexvalue'] - df_merged['Indexvalue'].rolling(30).mean()) / df_merged['Indexvalue'].rolling(30).std()

# Score combiné
df_merged['stress_score'] = df_merged['z_csd'] + df_merged['z_vstoxx']

# Plot
import matplotlib.pyplot as plt
plt.figure(figsize=(14,6))
plt.plot(df_merged['date'], df_merged['stress_score'], label="Stress Score", color="purple")
plt.axhline(df_merged['stress_score'].quantile(0.90), color='red', linestyle='--', label='90th percentile')
plt.title("Combined Stress Score (CSD + VSTOXX)")
plt.xlabel("Date")
plt.ylabel("Stress Score (z)")
plt.legend()
plt.grid(True)
plt.show()