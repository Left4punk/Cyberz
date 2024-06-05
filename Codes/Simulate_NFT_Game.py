import numpy as np
import random
import pandas as pd
import sys
import matplotlib.pyplot as plt

def mission_outcome(success_ratio):

    random_chance = np.random.rand()
    
    return True if random_chance < success_ratio else False


def cyber_hacker_mission(hours):
    
    success_rate = 0.7

    mission_rewards = {
        2: {'BYTE': 34,  'success_multi': 0.6, 'multiplier': 1},
        4: {'BYTE': 46, 'success_multi': 0.1, 'multiplier': 2},
        8: {'BYTE': 78, 'success_multi': 0, 'multiplier': 5},
    }

    failure_rewards = {
        'BYTE': 0,
        'success_multi': 0,
        'multiplier': 0
    }

    mission_status = mission_outcome(success_rate)  # Sucess Chance

    if mission_status and hours in mission_rewards:  # Rewards for success mission
        rewards = mission_rewards[hours]
        

    else:  # rewards for failed mission
        rewards = failure_rewards

    BYTE_earned = rewards['BYTE'] 
    
    multiplier_status = mission_outcome(rewards['success_multi'])

    if multiplier_status:

        BYTE_earned = BYTE_earned * rewards['multiplier']

    return BYTE_earned, mission_status

def smuggler_mission(hours):
    
    success_rate = 0.5

    mission_rewards = {
        2: {'BYTE': 46,  'success_multi': 0.38, 'multiplier': 1},
        4: {'BYTE': 78, 'success_multi': 0.11, 'multiplier': 2},
        8: {'BYTE': 90, 'success_multi': 0.08, 'multiplier': 5},
    }

    failure_rewards = {
        'BYTE': 0,
        'success_multi': 0,
        'multiplier': 0
    }

    mission_status = mission_outcome(success_rate)  # Sucess Chance

    if mission_status and hours in mission_rewards:  # Rewards for success mission
        rewards = mission_rewards[hours]

    else:  # rewards for failed mission
        rewards = failure_rewards

    BYTE_earned = rewards['BYTE'] 
    
    multiplier_status = mission_outcome(rewards['success_multi'])

    if multiplier_status:

        BYTE_earned = BYTE_earned * rewards['multiplier']

    return BYTE_earned, mission_status

def bounty_hunting_mission(hours):
    
    success_rate = 0.4

    mission_rewards = {
        2: {'BYTE': 62,  'success_multi': 0.32, 'multiplier': 1},
        4: {'BYTE': 86, 'success_multi': 0.06, 'multiplier': 2},
        8: {'BYTE': 106, 'success_multi': 0.02, 'multiplier': 5},
    }

    failure_rewards = {
        'BYTE': 0,
        'success_multi': 0,
        'multiplier': 0
    }

    mission_status = mission_outcome(success_rate)  # Sucess Chance

    if mission_status and hours in mission_rewards:  # Rewards for success mission
        rewards = mission_rewards[hours]

    else:  # rewards for failed mission
        rewards = failure_rewards

    BYTE_earned = rewards['BYTE'] 
    
    multiplier_status = mission_outcome(rewards['success_multi'])

    if multiplier_status:

        BYTE_earned = BYTE_earned * rewards['multiplier']

    return BYTE_earned, mission_status


def run_mission(mission_time):
    
    ##mission types
    missions = [cyber_hacker_mission, smuggler_mission, bounty_hunting_mission]

    # mission selection
    selected_mission = random.choice(missions)
    selected_mission_name = selected_mission.__name__
    # list resource name

    # run executed mission
    BYTE_earned, mission_status = selected_mission(mission_time)


    return BYTE_earned, mission_status, selected_mission_name, mission_time


def main ():

    
    total_BYTE = 0
    accumulated_playtime = 0

    i = 0

    while i<1000000:

        mission_time = random.choice([2, 4, 8])

        BYTE_earned, mission_status, selected_mission_name, mission_time = run_mission(mission_time)
        
        total_BYTE += BYTE_earned
        accumulated_playtime += mission_time
        

        i+=1

    return total_BYTE, accumulated_playtime


if __name__ == '__main__':

    simulation_results = []
    
    for i in range (1000):

        total_BYTE, accumulated_playtime = main()

        simulation_results.append([total_BYTE, accumulated_playtime,i+1])

        print (f'Simulation #{i}')

    df_results = pd.DataFrame(simulation_results, columns= ['Total $BYTE','Total Playtime','Simulation Run'])

    df_results['$BYTE/h'] = df_results['Total $BYTE']/df_results['Total Playtime']

    df_results.to_csv('nft_emissions_results.csv')
    