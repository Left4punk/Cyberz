import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

## Loading Results
#df = pd.read_csv('xp_final_results_1000_runs.csv')

#df = pd.read_csv('bit_emissions_results_1000_runs.csv')

df = pd.read_csv('full_mission_emissions_results_1000_runs.csv')
#df = pd.read_csv('nft_emissions_results.csv')
#df['XP per Hour'] = df['Total XP'] / df['Total Play Time']


#df['BIT per Hour'] = df['Total Bits'] / df['Total Play Time']

df['Junk per Hour'] = df['Total Junk'] / df['Total Play Time']

plt.figure(figsize=(10, 6))
#sns.boxplot(x=df['XP per Hour'], color="lightblue")

sns.boxplot(x=df['Junk per Hour'], color="lightblue")

# Calculating mean & standard dev

mean_Junk_per_hour = df['Junk per Hour'].mean()
std_Junk_per_hour = df['Junk per Hour'].std()

#mean_plastic_per_hour = df['Plastic per Hour'].mean()
#std_plastic_per_hour = df['Plastic per Hour'].std()

#mean_xp_per_hour = df['XP per Hour'].mean()
#std_xp_per_hour = df['XP per Hour'].std()

#mean_Bit_per_hour = df['BIT per Hour'].mean()
#std_Bit_per_hour = df['BIT per Hour'].std()

#mean_BYTE_per_hour = df['$BYTE/h'].mean()
#std_BYTE_per_hour = df['$BYTE/h'].std()

# Adding Legend con w Mean and Std
plt.legend([f'Mean: {mean_Junk_per_hour:.2f}, Standard Deviation: {std_Junk_per_hour:.2f}'], loc='upper right')

plt.xlabel('Junk Emission per hour')
plt.title('Distribution of $Junk/Hour after 1000 simulations of 1500 missions')
plt.grid(False)

plt.savefig('Junk_per_hour.png')