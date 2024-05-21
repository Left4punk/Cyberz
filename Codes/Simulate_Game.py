import numpy as np
import random
import pandas as pd
import sys
import matplotlib.pyplot as plt


def roll_initial_bot_stats ():

    while True:
        size = random.randint(1, 15)
        haste = random.randint(1, min(15, 20 - size))
        crit = 21 - size - haste

        if (size<=15 and haste <= 15 and crit <= 15):
            
            return size, haste, crit

def roll_initial_bot_energy_res():

    energy_values = [100, 105, 110, 115, 120]
    odds = [0.55, 0.25, 0.10, 0.07, 0.03]
    
    energy = np.random.choice(energy_values, p=odds)

    resilience = random.randint(400, 600)

    return energy, resilience

def generate_bot (bot_name):

    ##rolling initial stats
    health = 100
    level = 1
    rarity = 'common'
    total_xp = 0
    total_playtime = 0
    size, haste, crit = roll_initial_bot_stats ()

    starting_energy, resilience = roll_initial_bot_energy_res()

    resource_yield_increase = 0.01*size
    energy = starting_energy + size
    mission_success_boost = 0.005*haste
    mission_crit_chance = 0.005*crit

    return {'name': bot_name, 'rarity': rarity, 'level': level, 'total_xp': total_xp, 'total_playtime': total_playtime,'health':health, 'size':size, 'crit':crit, 'haste':haste ,'resilience':resilience,
            'resource_yield_increase':resource_yield_increase, 'mission_success_boost':mission_success_boost, 'mission_crit_chance':mission_crit_chance, 'starting_energy':energy, 'current_energy':energy}


def roll_mission_destruction (resilience):

    destruction_number = random.randint(1,100000)

    return True if destruction_number<resilience else False

def mission_outcome(success_ratio):

    random_chance = random.random()
    
    return True if random_chance < success_ratio else False


def data_vaults_mission(hours, resilience,mission_success_boost):
    
    sucess_rate = 0.4 + mission_success_boost

    mission_rewards = {
        2: {'silicon_range': (3, 5), 'xp_hour': 50, 'bits_hour': 20, 'junk_hour': (2, 5)},
        4: {'silicon_range': (5, 10), 'xp_hour': 50, 'bits_hour': 20, 'junk_hour': (2, 5)},
        8: {'silicon_range': (10, 15), 'xp_hour': 50, 'bits_hour': 20, 'junk_hour': (2, 5)},
    }

    failure_rewards = {
        'xp_hour': 15,
        'bits_hour': 10,
        'junk_hour': (0,0),
        'silicon_reward': 0,
    }
    
    if roll_mission_destruction(resilience):
        
        return False, False, 0, 0, 0, 0, 0 ##we check first if the bot is to be destroyed
    
    mission_status = mission_outcome(sucess_rate)  # Sucess Chance

    # Check Bot Destruction
    
    energy_cost_hour = 4

    if mission_status and hours in mission_rewards:  # Rewards for success mission
        rewards = mission_rewards[hours]
        silicon_reward = random.randint(*rewards['silicon_range'])

    else:  # rewards for failed mission
        rewards = failure_rewards
        silicon_reward = rewards['silicon_reward']

    xp_earned = rewards['xp_hour'] * hours
    bits_earned = rewards['bits_hour'] * hours
    junk_earned = random.randint(*rewards.get('junk_hour', (0, 0))) * hours if 'junk_hour' in rewards else 0
    energy_cost = energy_cost_hour * hours

    return True, mission_status, silicon_reward, xp_earned, bits_earned, energy_cost, junk_earned

def refinery_mission(hours, resilience,mission_success_boost):
    
    sucess_rate = 0.5 + mission_success_boost

    mission_rewards = {
        2: {'metal_range': (4, 6), 'xp_hour': 40, 'bits_hour': 15, 'junk_hour': (2, 4)},
        4: {'metal_range': (7, 12), 'xp_hour': 40, 'bits_hour': 15, 'junk_hour': (2, 4)},
        8: {'metal_range': (14, 24), 'xp_hour': 40, 'bits_hour': 15, 'junk_hour': (2, 4)},
    }

    failure_rewards = {
        'xp_hour': 12,
        'bits_hour': 8,
        'junk_hour': (0,0),
        'metal_range': 0,
    }

    # Check Bot Destruction
    if roll_mission_destruction(resilience):
        
        return False, False, 0, 0, 0, 0, 0 ##we check first if the bot is to be destroyed
    
    mission_status = mission_outcome(sucess_rate)  # Sucess Chance

    energy_cost_hour = 3

    if mission_status and hours in mission_rewards:  # Rewards for success mission
        rewards = mission_rewards[hours]
        metal_reward = random.randint(*rewards['metal_range'])

    else:  # rewards for failed mission
        rewards = failure_rewards
        metal_reward = rewards['metal_range']

    xp_earned = rewards['xp_hour'] * hours
    bits_earned = rewards['bits_hour'] * hours
    junk_earned = random.randint(*rewards.get('junk_hour', (0, 0))) * hours if 'junk_hour' in rewards else 0
    energy_cost = energy_cost_hour * hours

    return True, mission_status, metal_reward, xp_earned, bits_earned, energy_cost, junk_earned


def plastic_mission(hours, resilience,mission_success_boost):
    
    sucess_rate = 0.6+mission_success_boost
    mission_rewards = {
        2: {'plastic_range': (5, 7), 'xp_hour': 30, 'bits_hour': 10, 'junk_hour': (2, 3)},
        4: {'plastic_range': (9, 14), 'xp_hour': 30, 'bits_hour': 10, 'junk_hour': (2, 3)},
        8: {'plastic_range': (18, 28), 'xp_hour': 30, 'bits_hour': 10, 'junk_hour': (2, 3)},
    }

    failure_rewards = {
        'xp_hour': 9,
        'bits_hour': 5,
        'junk_hour': (0,0),
        'plastic_range': 0,
    }

    # Check Bot Destruction
    if roll_mission_destruction(resilience):
        
        return False, False, 0, 0, 0, 0, 0 ##we check first if the bot is to be destroyed
    
    mission_status = mission_outcome(sucess_rate)  # Sucess/Failure Mission

    energy_cost_hour = 2

    if mission_status and hours in mission_rewards:  # Rewards for success mission
        rewards = mission_rewards[hours]
        plastic_reward = random.randint(*rewards['plastic_range'])

    else:  # rewards for failed mission
        rewards = failure_rewards
        plastic_reward = rewards['plastic_range']

    xp_earned = rewards['xp_hour'] * hours
    bits_earned = rewards['bits_hour'] * hours
    junk_earned = random.randint(*rewards.get('junk_hour', (0, 0))) * hours if 'junk_hour' in rewards else 0
    energy_cost = energy_cost_hour * hours

    return True, mission_status, plastic_reward, xp_earned, bits_earned, energy_cost, junk_earned

def mission_final_rewards (bits_earned, material_reward,resource_yield_increase,mission_crit_chance):

    total_bits = round(bits_earned * (1+resource_yield_increase),1)
    
    random_chance_mission = random.random()

    crit_mission = 2 if random_chance_mission < mission_crit_chance else 1

    total_material = material_reward * crit_mission

    return total_bits, total_material, crit_mission

def run_mission(bot, mission_time):
    
    resilience = bot['resilience']
    resource_yield_increase = bot['resource_yield_increase']
    mission_success_boost = bot['mission_success_boost']
    mission_crit_chance = bot['mission_crit_chance']
    bot_name = bot['name']
    ##mission types

    missions = [data_vaults_mission, refinery_mission, plastic_mission]

    # mission selection
    selected_mission = random.choice(missions)
    selected_mission_name = selected_mission.__name__
    # list resource name
    resource_names = {
        data_vaults_mission: 'Silicon',
        refinery_mission: 'Metal',
        plastic_mission: 'Plastic'
    }
    resource_name = resource_names[selected_mission]

    # run executed mission
    bot_status, mission_status, resource_reward, xp_earned, bits_earned, energy_cost, junk_earned = selected_mission(mission_time, resilience, mission_success_boost)
     
    if not bot_status: ##if bot has been destroyed we don't compute the mission rewards

        return False, bot_name, selected_mission_name, resource_name, mission_time, mission_status, resource_reward, xp_earned, bits_earned, energy_cost, junk_earned, 1
    
    # Final resource rewards
    total_bits, total_material, crit_mission = mission_final_rewards(bits_earned, resource_reward, resource_yield_increase, mission_crit_chance)

    return bot_status, bot_name, selected_mission_name, resource_name, mission_time, mission_status, total_material, xp_earned, total_bits, energy_cost, junk_earned, crit_mission


def recharge_energy(current_energy, max_energy):

    energy_needed = max_energy - current_energy

    time_needed = (energy_needed / 20) * 0.5  
    
    new_energy = current_energy + (time_needed * 40) 

    if new_energy > max_energy:
        new_energy = max_energy
    
    return new_energy, time_needed


def assign_skill_points(size, haste, crit):
    # random assignment of 2 skill points to size, haste, or crit

    for _ in range(2): 
        increase = random.choice(["size", "haste", "crit"])
        if increase == "size":
            size += 1
        elif increase == "haste":
            haste += 1
        else:
            crit += 1
    return size, haste, crit

def check_level_up(total_xp, total_bits, level, size, haste, crit):

    level_requirements = [
        {"level": 1, "xp_cost": 0, "bit_cost": 0},  # Initial Level
        {"level": 2, "xp_cost": 300, "bit_cost": 300},
        {"level": 3, "xp_cost": 900, "bit_cost": 650},
        {"level": 4, "xp_cost": 1800, "bit_cost": 1100},
        {"level": 5, "xp_cost": 3200, "bit_cost": 1800},
        {"level": 6, "xp_cost": 4225, "bit_cost": 1975},  
        {"level": 7, "xp_cost": 5320, "bit_cost": 2200},
        {"level": 8, "xp_cost": 6495, "bit_cost": 2565},
        {"level": 9, "xp_cost": 7775, "bit_cost": 3080},
        {"level": 10, "xp_cost": 9185, "bit_cost": 3745},
        {"level": 11, "xp_cost": 10765, "bit_cost": 4555},
        {"level": 12, "xp_cost": 12545, "bit_cost": 5515},
        {"level": 13, "xp_cost": 14575, "bit_cost": 6620},
        {"level": 14, "xp_cost": 16925, "bit_cost": 7875},
        {"level": 15, "xp_cost": 19665, "bit_cost": 9275},
        {"level": 16, "xp_cost": 22905, "bit_cost": 10825},
        {"level": 17, "xp_cost": 26780, "bit_cost": 12520},
        {"level": 18, "xp_cost": 31455, "bit_cost": 14365},
        {"level": 19, "xp_cost": 37165, "bit_cost": 16355},
        {"level": 20, "xp_cost": 44215, "bit_cost": 18495},
        {"level": 21, "xp_cost": 53005, "bit_cost": 20780},
        {"level": 22, "xp_cost": 64090, "bit_cost": 23215},
        {"level": 23, "xp_cost": 78205, "bit_cost": 25800},
        {"level": 24, "xp_cost": 96370, "bit_cost": 28525},
        {"level": 25, "xp_cost": 120000, "bit_cost": 31400},
    ]

    
    if level < len(level_requirements):
        
        next_level_req = level_requirements[level]  # Check requirements for next level

        if total_xp >= next_level_req["xp_cost"] and total_bits >= next_level_req["bit_cost"]:
            
            ## we assign the 2 skill points randomly
            size, haste, crit = assign_skill_points(size, haste, crit)

            total_bits -= next_level_req["bit_cost"]
            
            return True, level + 1, size, haste, crit, total_bits ##the true/false is needed as we'll need to upgrade the size/haste/crit variables
            
        else:

            return False, level, size, haste, crit, total_bits
    else:

        return False, level, size, haste, crit, total_bits  

def check_and_upgrade_rarity(level, rarity, total_junk, total_silicon, total_metal, total_plastic,resilience):
    rarity_levels = [5, 10, 15,20]  
    rarity_upgrade_requirements = {
        'common': {'junk_cost': 1465, 'silicon_cost': 230, 'metal_cost': 420, 'plastic_cost': 635},
        'uncommon': {'junk_cost': 2940, 'silicon_cost': 460, 'metal_cost': 845, 'plastic_cost': 1265},
        'rare': {'junk_cost': 0, 'silicon_cost': 1150, 'metal_cost': 2110, 'plastic_cost': 3165},
        'epic': {'junk_cost': 0, 'silicon_cost': 2305, 'metal_cost': 4225, 'plastic_cost': 6335}
    }

    next_rarity = {
        'common': 'uncommon',
        'uncommon': 'rare',
        'rare': 'epic',
        'epic': 'legendary'
    }
    resilience_multipliers = {
        'common':0.95,
        'uncommon':0.945,
        'rare':0.945,
        'epic':0.885
    }

    if level in rarity_levels and rarity in rarity_upgrade_requirements: ##check that we have the correct level + we are not legendary
        
        requirements = rarity_upgrade_requirements[rarity] ##requirements for the current rarity upgrade

        if (total_junk >= requirements['junk_cost'] and total_silicon >= requirements['silicon_cost'] and 
           total_metal >= requirements['metal_cost'] and total_plastic >= requirements['plastic_cost']):
            
            # update on the total resources remaining & rarity
            new_rarity = next_rarity[rarity]
            total_junk -= requirements['junk_cost']
            total_silicon -= requirements['silicon_cost']
            total_metal -= requirements['metal_cost']
            total_plastic -= requirements['plastic_cost']

            if rarity in resilience_multipliers:

                resilience = int(resilience * resilience_multipliers[rarity]) ##we upgrade rarity here

            return new_rarity, total_junk, total_silicon, total_metal, total_plastic, resilience
        else:

            return rarity, total_junk, total_silicon, total_metal, total_plastic, resilience
    else:
        # we dont have enough level to upgrade or we are at max rarity level
        return rarity, total_junk, total_silicon, total_metal, total_plastic, resilience


def check_all_bots_level_2(bots):
    
    all_level_2 = all(bot['level'] >= 2 for bot in bots) ## we check if all bots that are running the missions have reached level 5, if so returns false

    return all_level_2

def select_bot_for_leveling(bots):
    
    ## having reached level 5 for all bots, we will select the one that has the largest XP and we'll start leveling it exclusively

    bot_for_leveling = max(bots, key=lambda bot: bot['level'])
    return bot_for_leveling['name']


### functions to generate a new bot with rarity loss when a rare bot gets destroyed

def assign_additional_skill_points (size, haste, crit, additional_points):

    for _ in range (additional_points):

        increase = random.choice(["size","haste","crit"])

        if increase == "size":
            size +=1
        
        elif increase == "hase":
            haste+=1
        
        else:
            crit +=1
    
    return size, haste, crit

def adjust_resilience_for_rarity (resilience, rarity):

    resilience_multipliers = {
        'common':1.0,
        'uncommon':0.95,
        'rare':0.9,
        'epic':0.85,
        'legendary':0.75
    }

    return int(resilience * resilience_multipliers[rarity])

def experience_for_level(level):
    level_requirements = [

        {"level": 5, "xp_cost": 3200},
        {"level": 10, "xp_cost": 9185},
        {"level": 15, "xp_cost": 19665},
        {"level": 20, "xp_cost": 44215},
    ]
    return level_requirements[level-1]["xp_cost"]

def generate_bot_when_destroyed(bot_name, rarity, level, total_playtime):

    health = 100
    total_xp = experience_for_level(level)
    base_size, base_haste, base_crit = roll_initial_bot_stats()
    starting_energy, base_resilience = roll_initial_bot_energy_res()

    # Calculate additional skill points based on the level
    additional_points = level * 2
    size, haste, crit = assign_additional_skill_points(base_size, base_haste, base_crit, additional_points)

    # Adjust resilience based on rarity
    resilience = adjust_resilience_for_rarity(base_resilience, rarity)

    resource_yield_increase = 0.01 * size
    energy = starting_energy + size
    mission_success_boost = 0.005 * haste
    mission_crit_chance = 0.005 * crit

    bot = {
        'name': bot_name, 'rarity': rarity, 'level': level, 'total_xp': total_xp, 'total_playtime': total_playtime, 
        'health': health, 'size': size, 'crit': crit, 'haste': haste, 'resilience': resilience,
        'resource_yield_increase': resource_yield_increase, 'mission_success_boost': mission_success_boost, 
        'mission_crit_chance': mission_crit_chance, 'starting_energy': energy, 'current_energy': energy
    }

    return bot


def main():

    bots = []
    bot_name_start = 1

    for _ in range (4):
        bot_name = f'bot{bot_name_start}'
        bot = generate_bot(bot_name)
        bots.append(bot)
        bot_name_start +=1
    
    #rarity, level, health, size, haste, crit, resilience, max_energy, resource_yield_increase, mission_success_boost, mission_crit_chance, starting_energy = generate_bot(bot_name)
    
    accumulated_results = []  # list to store mission progress
    individual_missions = []
    bot_stats = []

    total_junk = 0
    total_bits = 0
    total_plastic = 0
    total_metal = 0
    total_silicon = 0
    accumulated_playtime = 0

    all_bots_level_2 = False
    bot_to_max_level = None

    i = 1

    while i <= 1500:

        for bot in list(bots):

            mission_time = random.choice([2, 4, 8])
 
            bot_status, bot_name, selected_mission_name, resource_name, mission_time, mission_status, total_material, xp_earned, final_bits, energy_cost, junk_earned, crit_mission = run_mission(bot, mission_time)
            
            ##if I can't complete the mission I need to recharge my bot
            if (bot['current_energy'] < energy_cost): ## special "recharge energy" mission
            
                new_energy, recharge_time = recharge_energy(bot['current_energy'], bot['starting_energy'])

                bot['total_playtime'] += recharge_time  # adding the needed time to recharge to the total time
                accumulated_playtime += recharge_time
                bot['current_energy'] = new_energy

                selected_mission_name = 'Energy Recharge'
                resource_name = 'Energy'
                mission_time = recharge_time
                mission_status = True
                crit_mission = 1
                total_material = 0
                xp_earned = 0
                final_bits = 0
                energy_cost = 0
                junk_earned = 0
            
                individual_missions.append ([bot_name,selected_mission_name, resource_name, mission_time, mission_status, crit_mission, total_material, xp_earned, final_bits, energy_cost, junk_earned])
                accumulated_results.append([bot_name,selected_mission_name, resource_name, mission_time, mission_status, energy_cost, crit_mission,
                        total_plastic, total_metal, total_silicon, bot['total_xp'], total_bits, total_junk, bot['current_energy']])
                
                continue

            ## else we compute the mission results
            
            ## check if the bot has been destroyed
            if not bot_status: 
                
                bots.remove(bot)
                new_bot_name = f'bot{bot_name_start}'
                current_rarity = bot['rarity']
                total_playtime = bot['total_playtime']

                ##define the levels to default to
                rarity_min_levels = {
                    'common': 1,
                    'uncommon':6,
                    'rare':11,
                    'epic':16,
                    'legendary':21
                }

                if current_rarity != 'common':

                    if random.random() <= 0.3: ## 30% chance to keep the same rarity
                        
                        new_rarity = current_rarity
                        new_level = rarity_min_levels[new_rarity] ##setting up the lowest tier of leveling within that rarity
                    
                    else: ## 70% chance to drop 1 rarity tier
                        
                        rarity_order = ['common','uncommon','rare','epic','legendary']
                        rarity_index = rarity_order.index(current_rarity) ##checking which rarity we are in

                        if rarity_index > 1: ## we only care about rare epic and legendary downgrades as if we go from uncommon -> common we just create a new bot and ggz
                            new_rarity = rarity_order[rarity_index-1] ## we drop 1 rarity tier
                            new_level = rarity_min_levels[new_rarity] ## setting up the lowest tier of leveling within the new rarity
                        
                        else:
                            new_bot = generate_bot(new_bot_name) ##generating the new bot with the name
                            bots.append(new_bot)
                            bot_name_start += 1
                            continue
                else:
                    new_bot = generate_bot(new_bot_name) ##generating the new bot with the name
                    bots.append(new_bot)
                    bot_name_start += 1
                    continue
                
                new_bot = generate_bot_when_destroyed(new_bot_name, new_rarity, new_level, total_playtime)
                bots.append(new_bot)
                bot_name_start += 1
                
                ##we recheck if the destroyed bot was the one to keep maxing or not
                all_bots_level_2 = check_all_bots_level_2(bots)

                if all_bots_level_2:
                    bot_to_max_level = select_bot_for_leveling(bots)

                continue
            ## check if the bot has been destroyed
            
            individual_missions.append ([bot_name, selected_mission_name, resource_name, mission_time, mission_status, crit_mission, total_material, xp_earned, final_bits, energy_cost, junk_earned])
        
            ## adding mission gains to general counters
            bot['total_playtime'] += mission_time
            accumulated_playtime += mission_time
            bot['total_xp'] += xp_earned
            total_junk += junk_earned
            total_bits += final_bits
            bot['current_energy'] -= energy_cost

            if resource_name == 'Plastic':
                total_plastic += total_material
            elif resource_name == 'Metal':
                total_metal += total_material
            else:
                total_silicon += total_material
            ## adding mission gains to general counters
            
            ##checking if the bot can level up
            
            ## here we include a logic where we check if all the bots are already leveled up to level 5, we will start only focusing on the selected bot to max level
            if all_bots_level_2: ## if all bots are level 5, then we focus on the bot to max_level
                
                if bot_name == bot_to_max_level:

                    can_level_up, new_level, new_size, new_haste, new_crit, updated_total_bits = check_level_up(bot['total_xp'], total_bits, bot['level'], bot['size'], bot['haste'], bot['crit'])

                    if can_level_up: ## if the bot that we are maxing can level up we change its parameters

                        bot['level'] = new_level
                        bot['size'] = new_size
                        bot['haste'] = new_haste
                        bot['crit'] = new_crit
                        bot['resource_yield_increase'] = 0.01*bot['size']
                        bot['current_energy'] = bot['starting_energy'] + bot['size']
                        bot['mission_success_boost'] = 0.005*bot['haste']
                        bot['mission_crit_chance'] = 0.005*bot['crit']

                        total_bits = updated_total_bits ## substracting the bits

            else: ##if not all bots are up to level 5 we to keep leveling all
                    
                can_level_up, new_level, new_size, new_haste, new_crit, updated_total_bits = check_level_up(bot['total_xp'], total_bits, bot['level'], bot['size'], bot['haste'], bot['crit'])

                if can_level_up: ## if the bot that we are maxing can level up we change its parameters

                    bot['level'] = new_level
                    bot['size'] = new_size
                    bot['haste'] = new_haste
                    bot['crit'] = new_crit
                    bot['resource_yield_increase'] = 0.01*bot['size']
                    bot['current_energy'] = bot['starting_energy'] + bot['size']
                    bot['mission_success_boost'] = 0.005*bot['haste']
                    bot['mission_crit_chance'] = 0.005*bot['crit']

                    total_bits = updated_total_bits ## substracting the bits

        
            ##we check if we can upgrade rarity just after level up bc you can get to lvl 5 and be able to upgrade w/o doing any mission
            bot['rarity'], total_junk, total_silicon, total_metal, total_plastic, bot['resilience'] = check_and_upgrade_rarity(bot['level'], bot['rarity'], total_junk, total_silicon, total_metal, total_plastic, bot['resilience'])

            ##end leveling up the bot

            #print (bot_name)
            # Store the final values
            accumulated_results.append([bot_name,selected_mission_name, resource_name, mission_time, mission_status, energy_cost, crit_mission,
                        total_plastic, total_metal, total_silicon, bot['total_xp'], total_bits, total_junk, bot['current_energy'],accumulated_playtime, i])
            bot_stats.append ([bot['total_playtime'], bot['total_xp'], bot_name, bot['level'], bot['rarity'], bot['health'], 
                               bot['size'], bot['haste'], bot['crit'], bot['resilience'], bot['starting_energy'], bot['resource_yield_increase'], bot['mission_success_boost'], bot['mission_crit_chance'], i])
        
        ## here we check if all our 4 bots have reached level 5, if so we select which bot is going to be max leveled
        if not all_bots_level_2:

            all_bots_level_2 = check_all_bots_level_2(bots)

            if all_bots_level_2:

                bot_to_max_level = select_bot_for_leveling(bots)
            
        #print(selected_mission_name, resource_name, mission_time, mission_status, total_material, xp_earned, final_bits, energy_cost, junk_earned, crit_mission)
        
        i+=1

    # df creation to track
    columns_accumulated = ['Bot Name','Mission Name', 'Resource Name', 'Mission Time', 'Mission Status', 'Energy Cost', 'Crit Mission',
                'Total Plastic', 'Total Metal', 'Total Silicon', 'Total XP', 'Total Bits','Total Junk', 'Total Energy','Total Play Time','Game Round']
    
    columns_mission = ['Bot Name','Mission Name', 'Resource Name', 'Mission Time', 'Mission Status', 'Crit Mission',
                'Material Earned', 'XP Earned', 'Bits Earned', 'Energy Cost', 'Junk Earned']
    
    columns_stats = ['Total Play Time', 'Total XP','Bot Name', 'Level', 'Rarity', 'Health','Size','Haste','Crit','Resilience','Max Energy','Res. Yield Incr.','Mission Success Boost','Mission Crit Chance','Mission Number']

    df_results = pd.DataFrame(accumulated_results, columns=columns_accumulated)
    df_results.to_csv('accumulated_results.xlsx', index=False)

    df_missions =  pd.DataFrame(individual_missions, columns=columns_mission)
    df_missions.to_csv('missions_results.xlsx', index=False)

    df_bot_stats = pd.DataFrame(bot_stats, columns=columns_stats)
    df_bot_stats.to_csv('bot_stats.csv',index=False)

    df_missions_emissions = df_results[['Total Plastic','Total Metal','Total Silicon','Total Junk', 'Total Play Time']]
    df_bot_avg_xp = df_bot_stats[['Total Play Time','Total XP','Bot Name','Level']]
    #df_bot_avg_xp.to_csv('xp_control.csv',index=False)
    #plot_xp_over_time_all_bots(df_bot_stats)

    return df_bot_avg_xp


if __name__ == '__main__': 

    all_runs_data = []
    all_bots_data = []
    for i in range (1):
        print (f'Simulation #{i}')
        df_bot_progression = main()
        #last_emission_rows = df_mission_emissions.iloc[-1:].copy()
        last_four_rows = df_bot_progression.iloc[-4:].copy()
        #df_mission_emissions['Simulation Run'] = i+1
        df_bot_progression['Simulation Run'] = i+1

        #all_runs_data.append(last_emission_rows)
        all_bots_data.append(df_bot_progression)
    
    #final_emissions_df = pd.concat(all_runs_data, ignore_index=True)
    final_bots_df = pd.concat(all_bots_data, ignore_index=True)
    # Store DF
    #final_emissions_df.to_csv('full_mission_emissions_results_1000_runs.csv', index=False)
    final_bots_df.to_csv('final_bot_results_1000_runs.csv', index=False)
    #main()
    