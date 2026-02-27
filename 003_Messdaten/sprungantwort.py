#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 14:25:07 2026

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


#%% Störungen bei erhöhter FSK-Rate


folder_path = '005_sprungantwort'

file_TP = os.path.join(folder_path, 'STOERT1.CSV')

df_tp = pd.read_csv(file_TP)
plt.figure(figsize=(6, 2.5))
plt.plot(df_tp.iloc[:, 0]+1.1, df_tp.iloc[:, 1], color=my_green, linewidth=0.1)
#plt.title('Sprungantwort: Störung durch Erhöhung der FSK-Rate')
plt.xlabel('Zeit / s')
plt.ylabel('Spannung / V')
plt.grid(True)
#plt.legend()
plt.tight_layout()

# OPTION B: Falls Option A nicht reicht, manuell Platz unten schaffen:
# plt.subplots_adjust(bottom=0.2) 

plt.show()

#%% pgf

import pandas as pd
import os

folder_path = '005_sprungantwort'
file_TP = os.path.join(folder_path, 'STOERT1.CSV')

# Daten laden (Annahme: Spalte 0 ist Zeit, Spalte 1 ist Spannung)
df_tp = pd.read_csv(file_TP)

# Daten ausdünnen (Slicing)
# Jeder 20. Punkt reicht meistens völlig aus
df_export = df_tp.iloc[::10, [0, 1]].copy()
df_export.columns = ['time', 'voltage']

# Export
df_export.to_csv('sprung_stoerung.csv', index=False)


#%% einstellung von Vc
#R10 = 100, R11=100k, 750 auf 3k auf 750 (FSK-RAte = 10Hz)

folder_path = '005_sprungantwort'

file_TP = os.path.join(folder_path, 'SPR_TP01.CSV')

df_tp = pd.read_csv(file_TP)
plt.figure(figsize=(10, 4))
plt.plot(df_tp.iloc[:, 0]+0.1595, df_tp.iloc[:, 1], color=my_orange)
plt.title('Sprungantwort: Steuerspannung $V_c$')
plt.xlabel('Zeit [s]')
plt.ylabel('Spannung [V]')
plt.grid(True)
plt.legend()

#%% pgf


import pandas as pd
import os

# Pfade definieren
folder_path = '005_sprungantwort'
file_name = 'SPR_TP01.CSV'
output_path = 'sprung_vc.csv'

# Sicherstellen, dass der Ordner existiert
os.makedirs('Bilder', exist_ok=True)

# Daten laden
df_spr = pd.read_csv(os.path.join(folder_path, file_name))

# Neues DataFrame erstellen
df_export = pd.DataFrame()

# Zeit-Offset addieren (0.1595s)
df_export['time'] = df_spr.iloc[:, 0] + 0.1595
df_export['voltage'] = df_spr.iloc[:, 1]

# WICHTIG: Slicing auf ::50, damit LaTeX nicht abstürzt!
# Bei ::1 (alle Daten) wird PGFPlots sehr wahrscheinlich nichts anzeigen.
df_export.iloc[::50].to_csv(output_path, index=False)

print(f"Fertig! Datei gespeichert unter: {output_path}")


#%% Vc einzeiln


folder_path = '005_sprungantwort'
file_TP = os.path.join(folder_path, 'SPR_TP01.CSV')

# 1. Daten laden und Zeit-Offset korrigieren
df_tp = pd.read_csv(file_TP)
df_tp.iloc[:, 0] = df_tp.iloc[:, 0] + 0.1595

# 2. Masken für die beiden Ausschnitte erstellen
mask1 = (df_tp.iloc[:, 0] >= 0.0184) & (df_tp.iloc[:, 0] <= 0.02225)
mask2 = (df_tp.iloc[:, 0] >= 0.068) & (df_tp.iloc[:, 0] <= 0.074)

df_subset1 = df_tp.loc[mask1]
df_subset2 = df_tp.loc[mask2]

# 3. Subplots erstellen (1 Zeile, 2 Spalten)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# --- Linker Plot (Erster Ausschnitt) ---
ax1.plot(df_subset1.iloc[:, 0], df_subset1.iloc[:, 1], color=my_orange)
ax1.set_title('positiver Frequenzsprung')
ax1.set_xlabel('Zeit / s')
ax1.set_ylabel('Spannung [V]')
ax1.grid(True)
ax1.legend()

# --- Rechter Plot (Zweiter Ausschnitt) ---
ax2.plot(df_subset2.iloc[:, 0], df_subset2.iloc[:, 1], color=my_orange)
ax2.set_title('negativer Frequenzsprung')
ax2.set_xlabel('Zeit / s')
ax2.set_ylabel('Spannung / V')
ax2.grid(True)
ax2.legend()

# Layout optimieren, damit sich Titel/Achsen nicht überschneiden
plt.tight_layout()
plt.show()



#%% Srungantwort der verschiedene Filtertypen


folder_path = '005_sprungantwort'

file_BP = os.path.join(folder_path, 'SPR_BP.CSV')
file_BS = os.path.join(folder_path, 'SPR_BS01.CSV')
file_TP = os.path.join(folder_path, 'SPR_TP01.CSV')
file_HP = os.path.join(folder_path, 'SPR_HP01.CSV')

# --- BANDPASS (BP) ---
df_bp = pd.read_csv(file_BP)
plt.figure(figsize=(10, 4))
plt.plot(df_bp.iloc[:, 0], df_bp.iloc[:, 2], color='blue')
plt.title('Sprungantwort: Bandpass (BP)')
plt.xlabel('Zeit [s]')
plt.ylabel('Spannung [V]')
plt.grid(True)
plt.legend()

# --- BANDSPERRE (BS) ---
df_bs = pd.read_csv(file_BS)
plt.figure(figsize=(10, 4))
plt.plot(df_bs.iloc[:, 0], df_bs.iloc[:, 2], color='red')
plt.title('Sprungantwort: Bandsperre (BS)')
plt.xlabel('Zeit [s]')
plt.ylabel('Spannung [V]')
plt.grid(True)
plt.legend()

# --- TIEFPASS (TP) ---
df_tp = pd.read_csv(file_TP)
plt.figure(figsize=(10, 4))
plt.plot(df_tp.iloc[:, 0], df_tp.iloc[:, 2], color='green')
plt.title('Sprungantwort: Tiefpass (TP)')
plt.xlabel('Zeit [s]')
plt.ylabel('Spannung [V]')
plt.grid(True)
plt.legend()

# --- HOCHPASS (HP) ---
df_hp = pd.read_csv(file_HP)
plt.figure(figsize=(10, 4))
plt.plot(df_hp.iloc[:, 0], df_hp.iloc[:, 2], color='orange')
plt.title('Sprungantwort: Hochpass (HP)')
plt.xlabel('Zeit [s]')
plt.ylabel('Spannung [V]')
plt.grid(True)
plt.legend()


plt.show()

#%% tp


folder_path = '005_sprungantwort'

file_TP = os.path.join(folder_path, 'SPR_TP01.CSV')


df_tp_corr = pd.read_csv(file_TP)
df_tp_corr.iloc[:, 0] = df_tp_corr.iloc[:, 0] + 0.16

mask_start = (df_tp_corr.iloc[:, 0] >= 0.0175) & (df_tp_corr.iloc[:, 0] <= 0.024)
mask_end   = (df_tp_corr.iloc[:, 0] >= 0.068) & (df_tp_corr.iloc[:, 0] <= 0.078)

df_subset_start = df_tp_corr.loc[mask_start]
df_subset_end   = df_tp_corr.loc[mask_end]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(df_subset_start.iloc[:, 0], df_subset_start.iloc[:, 2], color=my_blue)
ax1.set_title('Positiver Sprung')
ax1.set_xlabel('Zeit / s')
ax1.set_ylabel('Spannung / V')
ax1.grid(True)
ax1.legend()

ax2.plot(df_subset_end.iloc[:, 0], df_subset_end.iloc[:, 2], color=my_blue)
ax2.set_title('Negativer Sprung')
ax2.set_xlabel('Zeit / s')
ax2.set_ylabel('Spannung / V')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()


#%% HP

folder_path = '005_sprungantwort'

file_TP = os.path.join(folder_path, 'SPR_HP01.CSV')


df_tp_corr = pd.read_csv(file_TP)
df_tp_corr.iloc[:, 0] = df_tp_corr.iloc[:, 0] + 0.12

mask_start = (df_tp_corr.iloc[:, 0] >= 0.0415) & (df_tp_corr.iloc[:, 0] <= 0.048)
mask_end   = (df_tp_corr.iloc[:, 0] >= 0.09275) & (df_tp_corr.iloc[:, 0] <= 0.10225)

df_subset_start = df_tp_corr.loc[mask_start]
df_subset_end   = df_tp_corr.loc[mask_end]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(df_subset_start.iloc[:, 0], df_subset_start.iloc[:, 2], color=my_red)
ax1.set_title('Positiver Sprung')
ax1.set_xlabel('Zeit / s')
ax1.set_ylabel('Spannung / V')
ax1.grid(True)
ax1.legend()

ax2.plot(df_subset_end.iloc[:, 0], df_subset_end.iloc[:, 2], color=my_red)
ax2.set_title('Negativer Sprung')
ax2.set_xlabel('Zeit / s')
ax2.set_ylabel('Spannung / V')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()


#%% BP

folder_path = '005_sprungantwort'

file_TP = os.path.join(folder_path, 'SPR_BP.CSV')


df_tp_corr = pd.read_csv(file_TP)
df_tp_corr.iloc[:, 0] = df_tp_corr.iloc[:, 0] +0.28

mask_start = (df_tp_corr.iloc[:, 0] >= 0.01725) & (df_tp_corr.iloc[:, 0] <= 0.02375)
mask_end   = (df_tp_corr.iloc[:, 0] >= 0.068) & (df_tp_corr.iloc[:, 0] <= 0.078)

df_subset_start = df_tp_corr.loc[mask_start]
df_subset_end   = df_tp_corr.loc[mask_end]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(df_subset_start.iloc[:, 0], df_subset_start.iloc[:, 2], color=my_green)
ax1.set_title('Positiver Sprung')
ax1.set_xlabel('Zeit / s')
ax1.set_ylabel('Spannung / V')
ax1.grid(True)
ax1.legend()

ax2.plot(df_subset_end.iloc[:, 0], df_subset_end.iloc[:, 2], color=my_green)
ax2.set_title('Negativer Sprung')
ax2.set_xlabel('Zeit / s')
ax2.set_ylabel('Spannung / V')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()



#%% BS

folder_path = '005_sprungantwort'

file_TP = os.path.join(folder_path, 'SPR_BS01.CSV')


df_tp_corr = pd.read_csv(file_TP)
df_tp_corr.iloc[:, 0] = df_tp_corr.iloc[:, 0] +0.245

mask_start = (df_tp_corr.iloc[:, 0] >= 0.0177) & (df_tp_corr.iloc[:, 0] <= 0.0242)
mask_end   = (df_tp_corr.iloc[:, 0] >= 0.068) & (df_tp_corr.iloc[:, 0] <= 0.078)

df_subset_start = df_tp_corr.loc[mask_start]
df_subset_end   = df_tp_corr.loc[mask_end]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(df_subset_start.iloc[:, 0], df_subset_start.iloc[:, 2], color=my_yellow)
ax1.set_title('Positiver Sprung')
ax1.set_xlabel('Zeit / s')
ax1.set_ylabel('Spannung / V')
ax1.grid(True)
ax1.legend()

ax2.plot(df_subset_end.iloc[:, 0], df_subset_end.iloc[:, 2], color=my_yellow)
ax2.set_title('Negativer Sprung')
ax2.set_xlabel('Zeit / s')
ax2.set_ylabel('Spannung / V')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()



#%%

folder_path = '005_sprungantwort'


file_TP = os.path.join(folder_path, 'SPR_BS01.CSV') 


# --- TIEFPASS (TP) ANALYSE ---
df_tp = pd.read_csv(file_TP)

plt.figure(figsize=(10, 4))
# Wir plotten Spalte 0 (Zeit) gegen Spalte 2 (Spannung)
plt.plot(df_tp.iloc[:, 0] +0.245, df_tp.iloc[:, 2], color='green', label='TP Rohdaten')

plt.title('Analyse: ')
plt.xlabel('Zeit [s]')
plt.ylabel('Spannung [V]')
plt.grid(True)
plt.show()

# Gib uns die ersten Zeilen aus, um zu sehen, ob die Zeit bei 0 startet
print(df_tp.head())
