#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 15:11:47 2026

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


#%%Vc untere Grenze 

folder_path = '005_sprungantwort'
file_200 = os.path.join(folder_path, 'FIN_200.CSV')
file_240 = os.path.join(folder_path, 'FIN_240.CSV')


df_200 = pd.read_csv(file_200)
df_240 = pd.read_csv(file_240)

# --- 2. Zeitbereiche festlegen (Beschneiden) ---
# Hier einfach die Werte anpassen: [Startzeit, Endzeit]
crop_200 = [-0.0915, 0.1285] 
crop_240 = [0.0, 0.22] # Beispielwerte für 240Hz

# --- 3. Masken anwenden ---
mask_200 = (df_200.iloc[:, 0] >= crop_200[0]) & (df_200.iloc[:, 0] <= crop_200[1])
mask_240 = (df_240.iloc[:, 0] >= crop_240[0]) & (df_240.iloc[:, 0] <= crop_240[1])

df_200_cut = df_200.loc[mask_200]
df_240_cut = df_240.loc[mask_240]

# --- 4. Plotten ---
plt.figure(figsize=(10, 4))

# Verschieben (Offset) machst du hier direkt beim x-Wert:
plt.plot(df_200_cut.iloc[:, 0] + 0.0915, df_200_cut.iloc[:, 1], 
         color=my_red, linewidth=0.1, label="Sprung auf 200Hz")

plt.plot(df_240_cut.iloc[:, 0] + 0.0, df_240_cut.iloc[:, 1], 
         color=my_blue, linewidth=0.1, label="Sprung auf 240Hz")

plt.title('Sprungantwort: $V_c$-Verhalten an der unteren Grenze')
plt.xlabel('Zeit / s')
plt.ylabel('Spannung / V')
plt.grid(True)

# Legende fixieren (Farben sichtbar machen)
leg = plt.legend()
for line in leg.get_lines():
    line.set_linewidth(2.0)

plt.show()


#%% vc obere Grenze


folder_path = '005_sprungantwort'
file_200 = os.path.join(folder_path, 'FIN_12.CSV')
file_240 = os.path.join(folder_path, 'FIN_13.CSV')


df_200 = pd.read_csv(file_200)
df_240 = pd.read_csv(file_240)

# --- 2. Zeitbereiche festlegen (Beschneiden) ---
# Hier einfach die Werte anpassen: [Startzeit, Endzeit]
crop_200 = [0.135, 0.355] 
crop_240 = [0.147, 0.367] # Beispielwerte für 240Hz

# --- 3. Masken anwenden ---
mask_200 = (df_200.iloc[:, 0] >= crop_200[0]) & (df_200.iloc[:, 0] <= crop_200[1])
mask_240 = (df_240.iloc[:, 0] >= crop_240[0]) & (df_240.iloc[:, 0] <= crop_240[1])

df_200_cut = df_200.loc[mask_200]
df_240_cut = df_240.loc[mask_240]

# --- 4. Plotten ---
plt.figure(figsize=(10, 4))
plt.plot(df_200_cut.iloc[:, 0] -0.135 , df_200_cut.iloc[:, 1], 
         color=my_blue, linewidth=0.1, label="Sprung auf 12kHz")

plt.plot(df_240_cut.iloc[:, 0] -0.1467, df_240_cut.iloc[:, 1], 
         color=my_red, linewidth=0.1, label="Sprung auf 13kHz")

plt.title('Sprungantwort: $V_c$-Verhalten an der oberen Grenze')
plt.xlabel('Zeit / s')
plt.ylabel('Spannung / V')
plt.grid(True)

# Legende fixieren (Farben sichtbar machen)
leg = plt.legend()
for line in leg.get_lines():
    line.set_linewidth(2.0)

plt.show()


#%%

folder_path = '005_sprungantwort'

file_TP = os.path.join(folder_path, 'FIN_3000.CSV')

df_tp = pd.read_csv(file_TP)
plt.figure(figsize=(10, 4))
plt.plot(df_tp.iloc[:, 0]+0.1595, df_tp.iloc[:, 1], color=my_orange)
plt.title('Sprungantwort: Steuerspannung $V_c$')
plt.xlabel('Zeit [s]')
plt.ylabel('Spannung [V]')
plt.grid(True)
plt.legend()



#%%

folder_path = '005_sprungantwort'
file_200  = os.path.join(folder_path, 'FIN_3000.CSV')

file_path4 = '005_sprungantwort/spice_sprungantwort.csv'
df4 = pd.read_csv(file_path4, sep='\t')



df_200 = pd.read_csv(file_200)
crop_200 = [0.245, 0.465] 
mask_200 = (df_200.iloc[:, 0] >= crop_200[0]) & (df_200.iloc[:, 0] <= crop_200[1])
df_200_cut = df_200.loc[mask_200]



# --- Plotten mit zwei Subplots untereinander ---
# figsize Höhe auf 8 erhöht, damit beide Plots genug Platz haben
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# --- Oberer Plot: Messung ---
ax1.plot(df_200_cut.iloc[:, 0] - 0.245, df_200_cut.iloc[:, 1], 
         color=my_orange, linewidth=0.1)
ax1.set_title('Sprungantwort: Messung')
ax1.set_xlabel('Zeit / s')  # Eigene Beschriftung für oben
ax1.set_ylabel('Spannung / V')
ax1.grid(True)



# --- Unterer Plot: Simulation ---
ax2.plot(df4['time'], df4['V(v_f3)'], 
         color=my_green, linewidth=1.5)
ax2.set_title('Sprungantwort: Simulation')
ax2.set_xlabel('Zeit / s')  # Eigene Beschriftung für unten
ax2.set_ylabel('Spannung / V')
ax2.grid(True)


# Abstand zwischen den Subplots optimieren
plt.tight_layout()

plt.show()



#%% TP


folder_path = '005_sprungantwort'
file_200 = os.path.join(folder_path, 'FIN_HPTP.CSV')

df_200 = pd.read_csv(file_200)
crop_200 = [0.3586, 0.5586] 
mask_200 = (df_200.iloc[:, 0] >= crop_200[0]) & (df_200.iloc[:, 0] <= crop_200[1])
df_200_cut = df_200.loc[mask_200]



# --- 4. Plotten ---
plt.figure(figsize=(10, 4))
plt.plot(df_200_cut.iloc[:, 0] - 0.3586, df_200_cut.iloc[:, 1], 
         color=my_blue, linewidth=0.5)


plt.xlabel('Zeit / s')
plt.ylabel('Spannung / V')
plt.grid(True)


#%% HP


folder_path = '005_sprungantwort'
file_200 = os.path.join(folder_path, 'FIN_HPTP.CSV')

df_200 = pd.read_csv(file_200)
crop_200 = [0.3586, 0.5586] 
mask_200 = (df_200.iloc[:, 0] >= crop_200[0]) & (df_200.iloc[:, 0] <= crop_200[1])
df_200_cut = df_200.loc[mask_200]



# --- 4. Plotten ---
plt.figure(figsize=(10, 4))
plt.plot(df_200_cut.iloc[:, 0] - 0.3586, df_200_cut.iloc[:, 2], 
         color=my_red, linewidth=0.5)


plt.xlabel('Zeit / s')
plt.ylabel('Spannung / V')
plt.grid(True)

#%% BP


folder_path = '005_sprungantwort'
file_200 = os.path.join(folder_path, 'FIN_BPBS.CSV')

df_200 = pd.read_csv(file_200)
crop_200 = [0.3964, 0.5964] 
mask_200 = (df_200.iloc[:, 0] >= crop_200[0]) & (df_200.iloc[:, 0] <= crop_200[1])
df_200_cut = df_200.loc[mask_200]



# --- 4. Plotten ---
plt.figure(figsize=(10, 4))
plt.plot(df_200_cut.iloc[:, 0] - 0.3964, df_200_cut.iloc[:, 1], 
         color=my_green, linewidth=0.5)


plt.xlabel('Zeit / s')
plt.ylabel('Spannung / V')
plt.grid(True)

#%%

folder_path = '005_sprungantwort'
file_200 = os.path.join(folder_path, 'FIN_BPBS.CSV')

df_200 = pd.read_csv(file_200)
crop_200 = [0.3964, 0.5964] 
mask_200 = (df_200.iloc[:, 0] >= crop_200[0]) & (df_200.iloc[:, 0] <= crop_200[1])
df_200_cut = df_200.loc[mask_200]



# --- 4. Plotten ---
plt.figure(figsize=(10, 4))
plt.plot(df_200_cut.iloc[:, 0] - 0.3964, df_200_cut.iloc[:, 2], 
         color=my_yellow, linewidth=0.5)


plt.xlabel('Zeit / s')
plt.ylabel('Spannung / V')
plt.grid(True)
