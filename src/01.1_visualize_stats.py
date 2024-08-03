import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
maf_df = pd.read_csv('maf.frq', delim_whitespace=True)
missing_df = pd.read_csv('missing.lmiss', delim_whitespace=True)
hwe_df = pd.read_csv('hwe.hwe', delim_whitespace=True)

# Calculate MAF for each marker
maf_df['MAF'] = maf_df.apply(lambda row: min(row['MAF'], 1 - row['MAF']), axis=1)

# Calculate Call Rate for each marker
missing_df['CallRate'] = 1 - missing_df['F_MISS']

# Plotting
plt.figure(figsize=(15, 5))

# MAF Distribution
plt.subplot(1, 3, 1)
sns.histplot(maf_df['MAF'], bins=30, kde=False)
plt.title('MAF Distribution')
plt.xlabel('MAF')
plt.ylabel('Frequency')

# Call Rate Distribution
plt.subplot(1, 3, 2)
sns.histplot(missing_df['CallRate'], bins=30, kde=False)
plt.title('Call Rate Distribution')
plt.xlabel('Call Rate')
plt.ylabel('Frequency')

# HWE p-value Distribution
plt.subplot(1, 3, 3)
sns.histplot(hwe_df['P_HWE'], bins=30, kde=False)
plt.title('HWE p-value Distribution')
plt.xlabel('HWE p-value')
plt.ylabel('Frequency')

# Show plots
plt.tight_layout()
plt.show()

# Calculate means and standard deviations
mean_maf = maf_df['MAF'].mean()
std_maf = maf_df['MAF'].std()
mean_call_rate = missing_df['CallRate'].mean()
std_call_rate = missing_df['CallRate'].std()
mean_hwe_p = hwe_df['P_HWE'].mean()
std_hwe_p = hwe_df['P_HWE'].std()

# Define the ranges within ±3 standard deviations
maf_lower, maf_upper = mean_maf - 3*std_maf, mean_maf + 3*std_maf
call_rate_lower, call_rate_upper = mean_call_rate - 3*std_call_rate, mean_call_rate + 3*std_call_rate
hwe_p_lower, hwe_p_upper = mean_hwe_p - 3*std_hwe_p, mean_hwe_p + 3*std_hwe_p

# Filter markers within the specified ranges
filtered_maf = maf_df[(maf_df['MAF'] >= maf_lower) & (maf_df['MAF'] <= maf_upper)]
filtered_call_rate = missing_df[(missing_df['CallRate'] >= call_rate_lower) & (missing_df['CallRate'] <= call_rate_upper)]
filtered_hwe = hwe_df[(hwe_df['P_HWE'] >= hwe_p_lower) & (hwe_df['P_HWE'] <= hwe_p_upper)]

# Join the filtered dataframes on the common marker identifier (assuming 'ID' is the common column)
selected_markers = filtered_maf.merge(filtered_call_rate, on='ID').merge(filtered_hwe, on='ID')

# Print the selected markers
print(selected_markers)

# Assuming 'chromosome' and 'position' columns are present in the merged DataFrame `selected_markers`
# and that these columns contain the necessary information.

# Example structure of the selected_markers DataFrame:
#   ID  chromosome  position  MAF  CallRate  P_HWE
# 0 rs1          1    12345  0.15      0.99  0.001
# 1 rs2          1    67890  0.20      0.95  0.050
# ...

# Create a BED format DataFrame
bed_df = selected_markers[['chromosome', 'position']].copy()

# BED format requires a 0-based start and a 1-based end. 
# So, we set start = position - 1 and end = position.
bed_df['start'] = bed_df['position'] - 1
bed_df['end'] = bed_df['position']

# Reorder columns to match BED format
bed_df = bed_df[['chromosome', 'start', 'end']]

# Save to a BED file
bed_df.to_csv('selected_markers.bed', sep='\t', header=False, index=False)

print("BED file saved as 'selected_markers.bed'.")

