import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Cargar los datos
bot_results_df = pd.read_csv('final_bot_results_1000_runs.csv')

# Conversión de 'Total Play Time' a días
bot_results_df['Total Play Time in Days'] = bot_results_df['Total Play Time'] / 24

simulations_display = [1, 999, 333, 666]

bot_results_df = bot_results_df[bot_results_df['Simulation Run'].isin(simulations_display)]

# Seleccionamos una paleta de colores más vibrante y atractiva
colors = plt.cm.viridis(np.linspace(0, 1, len(simulations_display)))
run_to_color = {run: color for run, color in zip(sorted(simulations_display), colors)}

# Offset para desplazar ligeramente los puntos en el eje y para cada simulación
offset_mapping = {run: offset for run, offset in zip(sorted(simulations_display), np.linspace(-0.3, 0.3, len(simulations_display)))}

# Gráfica 1: Ajustada para distinguir tanto el 'Bot Name' como la 'Simulation Run' con puntos ligeramente desplazados
plt.figure(figsize=(14, 6))
for bot_name in bot_results_df['Bot Name'].unique():
    for simulation_run in simulations_display:
        bot_data = bot_results_df[(bot_results_df['Bot Name'] == bot_name) & 
                                  (bot_results_df['Simulation Run'] == simulation_run)]
        adjusted_levels = bot_data['Level'] + offset_mapping[simulation_run]  # Añadir offset al nivel
        plt.scatter(bot_data['Total Play Time in Days'], adjusted_levels, 
                    label=f'{bot_name} - Sim {simulation_run}', alpha=0.6, s=10, 
                    color=run_to_color[simulation_run])

plt.title('Bot Level over Time')
plt.xlabel('Total Play Time (Days)')
plt.ylabel('Level')

# Ajustamos los ticks del eje X para que sean enteros
max_day = int(bot_results_df['Total Play Time in Days'].max())
plt.xticks(np.arange(0, max_day + 1, 25))

plt.legend(title='Bot Name - Simulation Run', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()

plt.savefig('Final Leveling Simulation.png')