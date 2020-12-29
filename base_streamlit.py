# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 06:34:35 2020

@author: Horri
"""

import streamlit as st
import random as r
import numpy as np
import pandas as pd

st.title('WFRP Dice Roller')

combat_bool = st.checkbox('Combat Roll?', False)
str_threshold = st.text_input('Input your Skill/Attribute Score', 40)
advantage = st.slider('Select your Advantage Modifer', -5,5,0)

int_threshold = None
str_roll = None
int_roll = None

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
    if roll > 10:
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
        
roll_dice()
determine_advantage(advantage)

def determine_critical(str_roll, int_roll):
    if str_roll[0] == str_roll[1]:
        
        if int_roll <= int_threshold:
            st.write('Critical Success!')
        else:
            st.write('Critical Failure!')
        if combat_bool == True:
            if int_roll <= 20:
                st.write('You catch a part of your anatomy. Lose one wound ignoring TB and AP')
            elif int_roll <= 40:
                st.write('Your weapon jars badly and suffers 1 damage, next round you act last regardless of initiatve')
            elif int_roll <= 60: 
                st.write('Next round your action suffers a -10 penalty')
            elif int_roll <= 70:
                st.write('You stumble badly, lose your movement next round')
            elif int_roll <= 80:
                st.write('You mishandle your weapon, miss your next action0')
            elif int_roll <= 90:
                st.write('You overextend yourself, suffer a Torn Muscle (Minor) injury (see page 179) this counts as a critical wound')
            elif int_roll <= 100:
                st.write('You complete mess up, hitting 1 random ally in range. If not possible, you are stunned')
            
def determine_hit_loc(str_roll, int_roll):
    loc = int(str_roll[1]+str_roll[0])
    st.title('Hit Location')
    if loc < 10:
        st.write('Head!')
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

def evaluate_dice(int_threshold, combat_bool, str_roll, int_roll):
    if int_roll <= int_threshold:
        st.write(f'{str_roll[0]} degress of Success!')
    else: 
        st.write(f'{str_roll[0]} degress of Failure!')
    if combat_bool == True:
        st.write('Remember, weapon skill tests are opposed check.')
        determine_hit_loc(str_roll, int_roll)

st.title('Results')      
determine_critical(str_roll, int_roll)
evaluate_dice(int_threshold, combat_bool, str_roll, int_roll)


        
    
    