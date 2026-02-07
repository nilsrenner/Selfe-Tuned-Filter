#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 14:34:28 2026

@author: nils
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

#%% HSB Farben

my_blue = (10/255,85/255,140/255)      #x/255 da HTMP bis 255 sene Farbscala hat und Matplotlib bis 1
my_red = (195/255, 5/255, 35/255)
my_green = (0/255, 145/255, 90/255)
my_yellow = (250/255, 190/255, 0/255)
my_orange = (240/255, 120/255, 35/255)
my_purple = (120/255, 100/255, 165/255)
my_green2 = (110/255, 165/255, 60/255)
my_blue2 = (50/255, 180/255, 200/255)



#%% Multipliziererausgang des PD mit 1000 und 1100Hz (Messung mit osc)
# Wir nehmen jetzt das mit Vpp=5V auch wenn die Amplitude der messung dann etwas höher ist


folder_path = '004_Phase_Detector'
file_multi_out = os.path.join(folder_path, 'multi_out_pHz3.CSV')

df = pd.read_csv(file_multi_out)
df.columns = df.columns.str.strip()

time = df['in s']
time = time - time.min()

time_ms = (time * 1000) - 0.16
c1 = df['C1 in V']
c2 = df['C2 in V'] #C2 ist bei diesen Messungen immer 1kHz


plt.figure(figsize=(10, 5)) 
plt.plot(time_ms, c1, color=my_blue, label='mult_out (Produkt)', ls='-')
plt.plot(time_ms, c2, color=my_red, label='f = 1kHz (Referenz)', ls='-')

plt.xlim(0, 10.01)

plt.title('Multipliziererausgang PD mit 1000Hz und 1100Hz (osc)')
plt.xlabel("Zeit [ms]")
plt.ylabel("Spannung [V]")
plt.legend(loc='upper right')
plt.grid(True, which='both', ls='--', lw=0.5)

plt.tight_layout()
plt.show()

#%%
folder_path = '004_Phase_Detector'
file_multi_out = os.path.join(folder_path, 'multi_out_pHz3.CSV')
file_pHz = '004_Phase_Detector/mult_freq_outputs.csv' 


df = pd.read_csv(file_multi_out)
df.columns = df.columns.str.strip()
time_ms = (df['in s'] - df['in s'].min()) * 1000 - 0.16

file_pHz = '004_Phase_Detector/mult_freq_outputs.csv' 
df_sim = pd.read_csv(file_pHz)
df_sim.columns = df_sim.columns.str.strip()


time_sim_ms = df_sim['time'] 
c1_1100hz = df_sim['out1100'] 


plt.figure(figsize=(10, 5)) 
plt.plot(time_ms, df['C1 in V'], color=my_blue, label='mult_out (real)', ls='-')
plt.plot(time_sim_ms, c1_1100hz, color='green', label='mult_out (sim)', ls='-')

plt.xlim(0, 10.01)
plt.title('Multipliziererausgang PD mit 1000Hz und 1100Hz (osc)')
plt.xlabel("Zeit [ms]")
plt.ylabel("Spannung [V]")
plt.legend(loc='upper right')
plt.grid(True, which='both', ls='--', lw=0.5)

plt.tight_layout()
plt.show()


#%% Ausgang des PD mit 1000 und 1100Hz (messung mit osc)

folder_path = '004_Phase_Detector'
file_pd_out = os.path.join(folder_path, 'pd_out_pHz2.CSV')

df = pd.read_csv(file_pd_out)
df.columns = df.columns.str.strip()

time = df['in s']
time = time - time.min()

time_ms = (time * 1000) - 0.15

c1 = df['C1 in V']
c2 = df['C2 in V']

plt.figure(figsize=(10, 5)) 
plt.plot(time_ms, c1+0.11, color=my_blue, label='pd_out (Produkt)+ Offset=13.57V', ls='-')
plt.plot(time_ms, c2, color=my_red, label='f = 1kHz (Referenz)', ls='-')

plt.xlim(0, 10.01)

plt.title('PD-Ausgang mit 1000Hz und 1100Hz (osc)')
plt.xlabel("Zeit [ms]")
plt.ylabel("Spannung [V]")
plt.legend(loc='upper right')
plt.grid(True, which='both', ls='--', lw=0.5)

plt.tight_layout()
plt.show()

#%%
folder_path = '004_Phase_Detector'
file_pd_out = os.path.join(folder_path, 'pd_out_pHz2.CSV')
file_sim_detec = '004_Phase_Detector/detec_freq_outputs.csv' # Deine neue Simulations-CSV


df = pd.read_csv(file_pd_out)
df.columns = df.columns.str.strip()

time_mess = df['in s'] - df['in s'].min()
time_ms = (time_mess * 1000) 

df_sim = pd.read_csv(file_sim_detec)
df_sim.columns = df_sim.columns.str.strip()


time_sim_ms = df_sim['time'] 
c_sim_detec = df_sim['detec1100']


plt.figure(figsize=(10, 5)) 
plt.plot(time_ms, df['C1 in V'] + 0.122, color=my_blue, label='pd_out (real) + Offset', ls='-')
plt.plot(time_ms, df['C2 in V'], color=my_red, label='f = 1kHz (Referenz)', ls='-')

plt.plot(time_sim_ms, c_sim_detec-2.528, color='green', label='pd_out (sim) + Offset', ls='-')

plt.xlim(0, 10.01)
plt.title('PD-Ausgang mit 1000Hz und 1100Hz (osc)')
plt.xlabel("Zeit [ms]")
plt.ylabel("Spannung [V]")
plt.legend(loc='upper right')
plt.grid(True, which='both', ls='--', lw=0.5)

plt.tight_layout()
plt.show()

#%%

folder_path = '004_Phase_Detector'
file_pd_out = os.path.join(folder_path, 'pd_out_pHz2.CSV')
file_sim_detec = '004_Phase_Detector/detec_freq_outputs.csv' # Deine neue Simulations-CSV

df = pd.read_csv(file_pd_out)
df.columns = df.columns.str.strip()


time_mess = df['in s'] - df['in s'].min()
time_ms = (time_mess * 1000) - 0.15

df_sim = pd.read_csv(file_sim_detec)
df_sim.columns = df_sim.columns.str.strip()

time_sim_ms = df_sim['time'] 
c_sim_detec = df_sim['detec1100']

plt.figure(figsize=(10, 5)) 
plt.plot(time_ms, df['C1 in V'] + 13.68, color=my_blue, label='pd_out (real) + Offset', ls='-')
plt.plot(time_sim_ms, c_sim_detec, color='green', label='pd_out (sim) + Offset', ls='-')

plt.xlim(0, 10.01)
plt.title('PD-Ausgang mit 1000Hz und 1100Hz (osc)')
plt.xlabel("Zeit [ms]")
plt.ylabel("Spannung [V]")
plt.legend(loc='upper right')
plt.grid(True, which='both', ls='--', lw=0.5)

plt.tight_layout()
plt.show()

