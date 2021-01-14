# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 06:34:35 2020

@author: Horri
"""

import streamlit as st
import random as r
import numpy as np
import pandas as pd

# # # # # # #

#left_col, right_col = st.beta_columns(2)

st.title('WFRP Dice Roller')

st.button('Roll!')
combat_bool = st.sidebar.checkbox('Combat Roll?', False)
weapon = st.sidebar.selectbox('Select your Weapon', ['Hand Weapon', 'Dagger', 'Pick', 'Long Bow', 'Handgun','Pistol'])
impale_trait = st.sidebar.checkbox('Impale Trait?', False)
damaging_trait = st.sidebar.checkbox('Damaging Trait?', False)
dangerous_trait = st.sidebar.checkbox('Dangerous Trait', False)
slow_trait = st.sidebar.checkbox('Slow Trait?', False)
strength_bonus = st.sidebar.text_input('Input Strength Bonus')


left_col, right_col = st.beta_columns(2)

str_threshold = st.text_input('Input your Skill/Attribute Score', 40)
advantage = st.slider('Select your Advantage Modifer', -5,5,0)

# # # # # # # 

int_threshold = None
str_roll = None
int_roll = None
hit_loc = None

def check_input_type(threshold):
    global int_threshold 
    
    try:
        int_threshold = int(str_threshold)
        if int_threshold < 101 | int_threshold > 0:
            return int_threshold
        else: 
            st.write('Error: Score outside range')
    except:
        st.write('Input Type Error')
        
check_input_type(str_threshold)
        
def roll_dice():
    global str_roll
    global int_roll
    
    roll = r.randint(1, 100)
    int_roll = roll
    if roll >= 10:
        str_roll = str(roll)
    else:
        str_roll = '0'+str(roll)
    
def determine_advantage(advantage):
    global str_threshold
    global int_threshold
    
    mod_advantage = advantage * 10
    int_threshold = int_threshold + mod_advantage
    st.write(f''' 
             ------ Rolled: {str_roll} ------ Threshold: {int_threshold} ------
             ''')
    
def fumble():
    if combat_bool == True:
       if int_roll <= 20:
           st.write('Fumble: You catch a part of your anatomy. Lose one wound ignoring TB and AP')
       elif int_roll <= 40:
           st.write('Fumble: Your weapon jars badly and suffers 1 damage, next round you act last regardless of initiatve')
       elif int_roll <= 60: 
           st.write('Fumble: Next round your action suffers a -10 penalty')
       elif int_roll <= 70:
           st.write('Fumble: You stumble badly, lose your movement next round')
       elif int_roll <= 80:
           st.write('Fumble: You mishandle your weapon, miss your next action')
       elif int_roll <= 90:
           st.write('Fumble: You overextend yourself, suffer a Torn Muscle (Minor) injury (see page 179) this counts as a critical wound')
       elif int_roll <= 100:
           st.write('Fumble: You complete mess up, hitting 1 random ally in range. If not possible, you are stunned')
           
critical_head_injuries = {
 'Dramatic Injury':[1,'A fine wound across the forehead and cheek. Gain 1 Bleeding Condition. Once the wound is healed, the impressive scar it leaves provides a bonus of +1 SL to appropriate social Tests. You can only gain this benefit once.'],
 'Minor Cut':[1,'The strike opens your cheek and blood flies. Gain 1 Bleeding Condition.'],
 'Poked Eye':[1,'The blow glances across your eye socket. Gain 1 Blinded condition.'],
 'Ear Bash':[1,'After a sickening impact, your ear is left ringing. Gain 1 Deafened Condition.'],
 'Rattling Blow':[2,'The blow floods your vision with flashing lights. Gain 1 Stunned Condition.'],
 'Black Eye':[2,'A solid blow hits your eye, leaving tears and pain. Gain 2 Blinded Conditions.'],
 'Sliced Ear':[2,'Your side of your head takes a hard blow, cutting deep into your ear. Gain 2 Deafened and 1 Bleeding Condition.'],
 'Struck Forehead':[2,'A solid blow hits your forehead. Gain 2 Bleeding Conditions and a Blinded Condition that cannot be removed until all Bleeding Conditions are removed.'],
 'Fractured Jaw':[3,'With a sickening crunch, pain fills your face as the blow fractures your jaw. Gain 2 Stunned Conditions. Suffer a Broken Bone (Minor) injury.'],
 'Major Eye Wound':[3,'The blow cracks across your eye socket. Gain 1 Bleeding Condition. Also gain 1 Blinded Condition that cannot be removed until you receive Medical Attention.'],
 'Major Ear Wound':[3,'The blow strikes deep into one ear. Suffer a permanent –20 penalty on all Tests relating to hearing. If you suffer this result again, your hearing is permanently lost as the second ear falls quiet. Only magic can heal this.'],
 'Broken Nose':[3,'A solid blow to the centre of your face causing blood to pour. Gain 2 Bleeding Conditions. Make a Challenging (+0) Endurance Test, or also gain a Stunned Condition. After this wound has healed, gain +1/–1 SL on social rolls, depending on context, unless Surgery is used to reset the nose.'],
 'Broken Jaw':[4,'The crack is sickening as the blow hits you under the chin, breaking your jaw. Gain 3 Stunned Conditions. Make a Challenging (+0) Endurance Test or gain an Unconscious Condition. Suffer a Broken Bone (Major) injury.'],
 'Concussive Blow':[4,'Your brain rattles in your skull as blood spurts from your nose and ears. Take 1 Deafened , 2 Bleeding , and 1d10 Stunned Conditions. Gain a Fatigued Condition that lasts for 1d10 days. If you receive another Critical Wound to your head while suffering this Fatigued Condition, make an Average (+20) Endurance Test or also gain an Unconscious Condition.'],
 'Smashed Mouth':[4,'With a sickening crunch, your mouth is suddenly filled with broken teeth and blood. Gain 2 Bleeding Conditions. Lose 1d10 teeth — Amputation (Easy).'],
 'Mangled Ear':[4,'Little is left of your ear as the blow tears it apart. You gain 3 Deafened and 2 Bleeding Conditions. Lose your ear —Amputation (Average).'],
 'Devastated Eye':[5,'A strike to your eye completely bursts it, causing extraordinary pain. Gain 3 Blinded , 2 Bleeding , and 1 Stunned Condition. Lose your eye — Amputation (Difficult).'],
 'Disfiguring Blow':[5,'The blow smashes your entire face, destroying your eye and nose in a cloud of blood. Gain 3 Bleeding , 3 Blinded and 2 Stunned Conditions. Lose your eye and nose — Amputation (Hard).'],
 'Mangled Jaw':[5,'The blow almost removes your jaw as it utterly destroys your tongue, sending teeth flying in a shower of blood. Gain 4 Bleeding and 3 Stunned Conditions. Make a Very Hard (–30) Endurance Test or gain an Unconscious Condition. Suffer a Broken Bone (Major) injury and lose your tongue and 1d10 teeth — Amputation (Hard).'],
 'Decapitated':[100,'Your head is entirely severed from your neck and soars through the air, landing 1d10 feet away in a random direction (see Scatter). Your body collapses, instantly dead.'],
 } 
           
def determine_critical_loc():
    crit_roll = r.randint(1, 100)
    if crit_roll <= 10:
        return critical_head_injuries['Dramatic Injury'][1]
    elif crit_roll <= 20:
        return critical_head_injuries['Minor Cut'][1]
    elif crit_roll <= 25: 
        return critical_head_injuries['Poked Eye'][1]
    elif crit_roll <= 30:
        return critical_head_injuries['Ear Bash'][1]
    elif crit_roll <= 35:
        return critical_head_injuries['Rattling Blow'][1]
    elif crit_roll <= 40:
        return critical_head_injuries['Black Eye'][1]
    elif crit_roll <= 45:
        return critical_head_injuries['Sliced Ear'][1]
    elif crit_roll <= 50:
        return critical_head_injuries['Struck Forehead'][1]
    elif crit_roll <= 55:
        return critical_head_injuries['Fractured Jaw'][1]
    elif crit_roll <= 60:
        return critical_head_injuries['Major Eye Wound'][1]
    elif crit_roll <= 65:
        return critical_head_injuries['Major Ear Wound'][1]
    elif crit_roll <= 70:
        return critical_head_injuries['Broken Nose'][1]
    elif crit_roll <= 75:
        return critical_head_injuries['Broken Jaw'][1]
    elif crit_roll <= 80:
        return critical_head_injuries['Concussive Blow'][1]
    elif crit_roll <= 85:
        return critical_head_injuries['Smashed Mouth'][1]
    elif crit_roll <= 90:
        return critical_head_injuries['Mangled Ear'][1]
    elif crit_roll <= 93:
        return critical_head_injuries['Devastated Eye'][1]
    elif crit_roll <= 96:
        return critical_head_injuries['Disfiguring Blow'][1]
    elif crit_roll <= 99:
        return critical_head_injuries['Mangled Jaw'][1]
    elif crit_roll <= 101:  
        return critical_head_injuries['Decapitated'][1]          

def determine_critical(str_roll, int_roll):
    if (str_roll[0] == str_roll[1]) or (impale_trait and int_roll % 10 == 0):
        if int_roll <= int_threshold: 
            var = determine_critical_loc()
            st.write(f'{var}')
        else:
            st.write('Critical Failure!')
            fumble()
           
def determine_hit_loc(str_roll, int_roll):
    global hit_loc
    loc = int(str_roll[1]+str_roll[0])
    st.title('Hit Location')
    if loc < 10:
        st.write('Head!')
        hit_loc = 'Head'
    elif loc < 25:
        st.write('Left Arm')
    elif loc < 45:
        st.write('Right Arm')
    elif loc < 80:
        st.write('Body')
    elif loc < 90:
        st.write('left Leg')
    elif loc < 101:
        st.write('Right Leg')

def validate_combat():
    try:
        if combat_bool:
            if strength_bonus == False:
                st.write('ERROR: Enter in your Strenght Bonus.')
    except:
        raise Exception('uh oh!')

def evaluate_dice(int_threshold, combat_bool, str_roll, int_roll):
    if int_roll <= int_threshold:
        st.write(f'{str_roll[0]} degree(s) of Success!')
    else: 
        st.write(f'{str_roll[0]} degree(s) of Failure!')
    if combat_bool == True:
        if validate_combat():
            determine_hit_loc(str_roll, int_roll)
            if dangerous_trait == True:
                if (str_roll[0] or str_roll[1]) == ('9' or 9):
                    fumble()
        
def determine_weapon():
    global strength_bonus
    weapon_list = {'Hand Weapon':4, 'Dagger':2, 'Pick':5, 'Long Bow':4, 'Handgun':9,'Pistol':8}
    if weapon in weapon_list.keys():
        if int_roll <= int_threshold:
            if weapon == ('Handgun' or 'Pistol'):
                st.write(f'{weapon_list[weapon]+int(str_roll[0])} dmg')
                if damaging_trait:
                    st.write(f'or {weapon_list[weapon]+int(str_roll[1])} dmg')
            else:
                st.write(f'{weapon_list[weapon]+int(str_roll[0])+int(strength_bonus)} dmg')
                if damaging_trait:
                    st.write(f'or {weapon_list[weapon]+int(str_roll[1])} dmg')
        else:
            if weapon == ('Handgun' or 'Pistol'):
                st.write(f'{weapon_list[weapon]} dmg')
            else:
                st.write(f'{weapon_list[weapon]+int(strength_bonus)} dmg')

# # # # # # #

st.title('Results')  
roll_dice()
determine_advantage(advantage)    
determine_critical(str_roll, int_roll)
evaluate_dice(int_threshold, combat_bool, str_roll, int_roll)
determine_weapon()






    
    