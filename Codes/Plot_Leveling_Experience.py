import numpy as np
import matplotlib.pyplot as plt

# Initial configuration for $BITs
total_bits = 229000  # Total $BITs available over 6 months
num_levels = 25  # Total number of levels to design

# Predefined costs for levels 1 through 5
predefined_bit_costs = np.array([0, 300, 650, 1100, 1800])

# Predefined XP requirements for the first 5 levels
initial_levels_xp = [300, 600, 900, 1400]

# Calculate total $BITs and XP spent to get 4 characters to level 5
bits_spent_initial_levels = np.sum(predefined_bit_costs) * 4
xp_spent_initial_levels = np.sum(initial_levels_xp)

# Maximum XP for reaching the maximum level
total_xp_max_level = 120000

# Remaining XP and $BITs for distribution between levels 6-25
remaining_xp = total_xp_max_level - xp_spent_initial_levels
remaining_bits = total_bits - bits_spent_initial_levels
remaining_levels = 20  # Levels from 6 to 25

# Initial and final increments for XP required between levels
initial_increment = 1.05
final_increment = 1.3

# Increments as a linear scale between initial and final increments
xp_increments = np.linspace(initial_increment, final_increment, remaining_levels)

# Calculating and adjusting XP for levels 6-25
adjusted_req_xp = [initial_levels_xp[-1]]  # Start with the XP required for level 5
for i in range(1, remaining_levels + 1):
    new_xp = adjusted_req_xp[-1] * xp_increments[i - 1]
    adjusted_req_xp.append(new_xp)

# Adjust the XP values using the calculated total
xp_adj_factor = remaining_xp / sum(adjusted_req_xp)
adjusted_req_xp = [x * xp_adj_factor for x in adjusted_req_xp]

# Calculate the accumulated XP for each level
accumulated_xp = np.cumsum([0] + initial_levels_xp + adjusted_req_xp[1:]).tolist()

# For $BITs, we use a quadratic increase starting from level 6
bit_costs = predefined_bit_costs.tolist()
last_bit_cost = predefined_bit_costs[-1]
for i in range(6, num_levels + 1):
    # Quadratic increase from the last known bit cost
    cost = last_bit_cost + (i - 5)**2 * remaining_bits / sum((np.arange(6, num_levels + 1) - 5)**2)
    bit_costs.append(cost)
    last_bit_cost = cost

# Now we have both XP and $BIT requirements, let's plot them
plt.figure(figsize=(12, 6))

# Plotting $BIT requirements
plt.plot(range(1, num_levels + 1), bit_costs, label='Required $BIT', color='red', marker='o')

# Plotting XP requirements
plt.plot(range(1, num_levels + 1), accumulated_xp, label='Accumulated XP', color='blue', marker='x')

# Adding labels and title
plt.title('Leveling Requirements: $BIT and XP')
plt.xlabel('Level')
plt.ylabel('Requirement')
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5)
plt.tight_layout()

# Save the plot as a file
plt.savefig("Leveling Experience.png")

# Show the plot
plt.close()