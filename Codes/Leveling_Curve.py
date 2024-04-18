import numpy as np
import matplotlib.pyplot as plt

# Valores iniciales de experiencia para los primeros 5 niveles
initial_levels = [300, 600, 900, 1400]

# XP máxima para alcanzar el nivel máximo
total_xp_max_level = 120000

# Calculamos la XP acumulada hasta el nivel 5
accumulated_initial_xp = sum(initial_levels)

# XP restante para distribuir entre los niveles 6-25
remaining_xp = total_xp_max_level - accumulated_initial_xp
remaining_levels = 20  # Niveles restantes

# Incremento inicial y final para la experiencia requerida entre niveles
initial_increment = 1.05
final_increment = 1.3

# Calculamos los incrementos como una escala lineal entre los incrementos inicial y final
increments = np.linspace(initial_increment, final_increment, remaining_levels)

# Calculamos y ajustamos la experiencia para los niveles 6-25
adjusted_req_exp = [initial_levels[-1]]  # Empezamos con la experiencia requerida para el nivel 5
for i in range(1, remaining_levels + 1):
    new_xp = adjusted_req_exp[-1] * increments[i - 1]
    adjusted_req_exp.append(new_xp)

# Recalculamos el factor de ajuste basado en la XP total calculada
total_exp_adj_calculated = sum(adjusted_req_exp) + accumulated_initial_xp
adj_factor = total_xp_max_level / total_exp_adj_calculated

# Ajustamos los valores de experiencia necesarios usando el factor de ajuste
adj_needed_xp = [x * adj_factor for x in adjusted_req_exp]

# Calculamos la XP acumulada para cada nivel
final_acc_xp = np.cumsum([0] + initial_levels + adj_needed_xp[1:]).tolist()

print (final_acc_xp)
# Niveles totales para el gráfico
total_levels = list(range(1, 26))

# Generamos el gráfico
plt.figure(figsize=(10, 6))
plt.plot(total_levels, final_acc_xp, marker='o', linestyle='-', color='b')
plt.title('Accumulated XP per Level')
plt.xlabel('Level')
plt.ylabel('Accumulated XP')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.tight_layout()

# Mostramos el gráfico
plt.savefig("Leveling Progression.png")