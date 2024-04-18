import numpy as np

# Initial configuration
total_bits = 229000  # Total $BITs available over 6 months
num_levels = 25  # Total number of levels to design

# Your predefined costs for levels 1 through 5
predefined_costs = np.array([0, 300, 650, 1100, 1800])

# Calculate the total $BITs spent to get 4 characters to level 5
bits_spent_initial_levels = np.sum(predefined_costs) * 4

# Calculate the remaining $BITs for leveling one character from level 5 to level 25
bits_remaining_for_advanced_leveling = total_bits - bits_spent_initial_levels

# For levels 6 to 25, we define a quadratic function to calculate progressively higher costs
# Assume a form: cost = a * (level - 5)^2 for simplicity and to ensure it's always increasing
# We'll start our costs at a point higher than the cost for level 5 to ensure it's more expensive

# Generate levels array from 6 to 25
levels_advanced = np.arange(6, num_levels + 1)

# We use the square of the difference from level 5 to ensure progression
costs_advanced_levels = (levels_advanced - 5)**2

# Adjust the costs to fit within the remaining $BITs budget
# Find the scaling factor that makes the last level fit the remaining budget
last_level_cost = predefined_costs[-1] + 100  # Start slightly higher than the last predefined cost
scaling_factor = (bits_remaining_for_advanced_leveling - last_level_cost) / sum(costs_advanced_levels)
costs_advanced_levels_scaled = costs_advanced_levels * scaling_factor + last_level_cost

# Combine initial and advanced costs for a complete view
total_costs = np.concatenate((predefined_costs, costs_advanced_levels_scaled))

# Output the costs per level
for level, cost in enumerate(total_costs, start=1):
    print(f"Level {level}: {cost:.2f} $BITs")

# Check the total $BITs needed to level one character to 25 including the initial leveling of 4 characters
total_cost = np.sum(predefined_costs) * 4 + np.sum(costs_advanced_levels_scaled)
print(f"\nTotal $BITs required to level one character to 25: {total_cost:.2f}")