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


#%% pgf


import pandas as pd
import os

folder_path = '005_sprungantwort'
output_folder = 'Bilder'
os.makedirs(output_folder, exist_ok=True)

# Dateien laden
df_200 = pd.read_csv(os.path.join(folder_path, 'FIN_200.CSV'))
df_240 = pd.read_csv(os.path.join(folder_path, 'FIN_240.CSV'))

# --- 200 Hz Verarbeitung ---
crop_200 = [-0.0915, 0.1285] 
mask_200 = (df_200.iloc[:, 0] >= crop_200[0]) & (df_200.iloc[:, 0] <= crop_200[1])
df_200_final = pd.DataFrame({
    'time': df_200.loc[mask_200].iloc[:, 0] + 0.0915, 
    'voltage': df_200.loc[mask_200].iloc[:, 1]
})
df_200_final.iloc[::20].to_csv(os.path.join(output_folder, 'sprung_vc_200.csv'), index=False)

# --- 240 Hz Verarbeitung ---
crop_240 = [0.0, 0.22]
mask_240 = (df_240.iloc[:, 0] >= crop_240[0]) & (df_240.iloc[:, 0] <= crop_240[1])
df_240_final = pd.DataFrame({
    'time': df_240.loc[mask_240].iloc[:, 0], # Offset ist hier 0
    'voltage': df_240.loc[mask_240].iloc[:, 1]
})
df_240_final.iloc[::20].to_csv(os.path.join(output_folder, 'sprung_vc_240.csv'), index=False)

print("Vergleichsdaten für Vc (200Hz & 240Hz) exportiert.")






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

#%% pgf


import pandas as pd
import os

folder_path = '005_sprungantwort'
output_folder = 'Bilder'
os.makedirs(output_folder, exist_ok=True)

# Dateien laden
df_12 = pd.read_csv(os.path.join(folder_path, 'FIN_12.CSV'))
df_13 = pd.read_csv(os.path.join(folder_path, 'FIN_13.CSV'))

# --- 12 kHz Verarbeitung (Offset 0.135) ---
crop_12 = [0.135, 0.355] 
mask_12 = (df_12.iloc[:, 0] >= crop_12[0]) & (df_12.iloc[:, 0] <= crop_12[1])
df_12_final = pd.DataFrame({
    'time': df_12.loc[mask_12].iloc[:, 0] - 0.135, 
    'voltage': df_12.loc[mask_12].iloc[:, 1]
})
df_12_final.iloc[::20].to_csv(os.path.join(output_folder, 'sprung_vc_12khz.csv'), index=False)

# --- 13 kHz Verarbeitung (Offset 0.1467) ---
crop_13 = [0.147, 0.367]
mask_13 = (df_13.iloc[:, 0] >= crop_13[0]) & (df_13.iloc[:, 0] <= crop_13[1])
df_13_final = pd.DataFrame({
    'time': df_13.loc[mask_13].iloc[:, 0] - 0.1467,
    'voltage': df_13.loc[mask_13].iloc[:, 1]
})
df_13_final.iloc[::20].to_csv(os.path.join(output_folder, 'sprung_vc_13khz.csv'), index=False)

print("Letzte Vergleichsdaten (12kHz & 13kHz) erfolgreich exportiert.")







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


#%% pgf

import pandas as pd
import os

# Pfade
folder_path = '005_sprungantwort'
file_200 = os.path.join(folder_path, 'FIN_3000.CSV')
file_sim = '005_sprungantwort/spice_sprungantwort.csv'

# 1. Messung verarbeiten
df_200 = pd.read_csv(file_200)
crop_200 = [0.245, 0.465]
# Maske anwenden wie in deinem Code
mask_200 = (df_200.iloc[:, 0] >= crop_200[0]) & (df_200.iloc[:, 0] <= crop_200[1])
df_mess_cut = df_200.loc[mask_200].copy()

# Zeit-Offset korrigieren (Beginn bei 0)
df_mess_export = pd.DataFrame()
df_mess_export['time'] = df_mess_cut.iloc[:, 0] - 0.245
df_mess_export['voltage'] = df_mess_cut.iloc[:, 1]

# 2. Simulation verarbeiten (Achtung: Tab-Separator laut deinem Code)
df_sim = pd.read_csv(file_sim, sep='\t')
df_sim_export = pd.DataFrame()
df_sim_export['time'] = df_sim['time']
df_sim_export['voltage'] = df_sim['V(v_f3)']

# Export mit Slicing für LaTeX Performance
os.makedirs('Bilder', exist_ok=True)
df_mess_export.iloc[::20].to_csv('sprung_fin_mess.csv', index=False)
df_sim_export.iloc[::20].to_csv('sprung_fin_sim.csv', index=False)








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

#%% bs

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

#%%  pgf


import pandas as pd
import os

# Ordner definieren
folder_path = '005_sprungantwort'
output_folder = 'Bilder'
os.makedirs(output_folder, exist_ok=True)

# --- 1. Tiefpass (TP) und Hochpass (HP) aus FIN_HPTP.CSV ---
file_hptp = os.path.join(folder_path, 'FIN_HPTP.CSV')
if os.path.exists(file_hptp):
    df_hptp = pd.read_csv(file_hptp)
    crop_hptp = [0.3586, 0.5586]
    mask_hptp = (df_hptp.iloc[:, 0] >= crop_hptp[0]) & (df_hptp.iloc[:, 0] <= crop_hptp[1])
    df_cut = df_hptp.loc[mask_hptp].copy()
    
    # Tiefpass exportieren (Spalte 1)
    df_tp = pd.DataFrame()
    df_tp['time'] = df_cut.iloc[:, 0] - 0.3586
    df_tp['voltage'] = df_cut.iloc[:, 1]
    df_tp.iloc[::20].to_csv(os.path.join(output_folder, 'sprung_final_tp.csv'), index=False)
    
    # Hochpass exportieren (Spalte 2)
    df_hp = pd.DataFrame()
    df_hp['time'] = df_cut.iloc[:, 0] - 0.3586
    df_hp['voltage'] = df_cut.iloc[:, 2]
    df_hp.iloc[::20].to_csv(os.path.join(output_folder, 'sprung_final_hp.csv'), index=False)

# --- 2. Bandpass (BP) und Bandsperre (BS) aus FIN_BPBS.CSV ---
file_bpbs = os.path.join(folder_path, 'FIN_BPBS.CSV')
if os.path.exists(file_bpbs):
    df_bpbs = pd.read_csv(file_bpbs)
    crop_bpbs = [0.3964, 0.5964]
    mask_bpbs = (df_bpbs.iloc[:, 0] >= crop_bpbs[0]) & (df_bpbs.iloc[:, 0] <= crop_bpbs[1])
    df_cut = df_bpbs.loc[mask_bpbs].copy()
    
    # Bandpass exportieren (Spalte 1)
    df_bp = pd.DataFrame()
    df_bp['time'] = df_cut.iloc[:, 0] - 0.3964
    df_bp['voltage'] = df_cut.iloc[:, 1]
    df_bp.iloc[::20].to_csv(os.path.join(output_folder, 'sprung_final_bp.csv'), index=False)
    
    # Bandsperre exportieren (Spalte 2)
    df_bs = pd.DataFrame()
    df_bs['time'] = df_cut.iloc[:, 0] - 0.3964
    df_bs['voltage'] = df_cut.iloc[:, 2]
    df_bs.iloc[::20].to_csv(os.path.join(output_folder, 'sprung_final_bs.csv'), index=False)

print("Alle 4 CSV-Dateien wurden erfolgreich im Ordner 'Bilder/' gespeichert.")

