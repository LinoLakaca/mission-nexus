import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import json
import requests

# --- 1. UČITAVANJE ---
# Koristimo točne putanje koje je generator ispisao
df_gps = pd.read_csv('moji_mars_podaci/mars_lokacije.csv', sep=';', decimal=',')
df_uzorci = pd.read_csv('moji_mars_podaci/mars_uzorci.csv', sep=';', decimal=',')
df = pd.merge(df_gps, df_uzorci, on='ID_Uzorka')

# --- 2. ČIŠĆENJE ANOMALIJA ---
# Mičemo nemoguća očitanja (npr. Temp 150C) kako grafovi ne bi bili izobličeni
df_cisto = df[df['Temp_Tla_C'] < 100].copy()

# --- 3. IZRADA GRAFOVA ---

# Graf 1: Odnos temperature (X) i vlage (Y)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cisto, x='Temp_Tla_C', y='H2O_Postotak', hue='Metan_Senzor')
plt.savefig('graph1_temp_h2o.png')

# Graf 2: Geografska karta dubine bušenja
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', hue='Dubina_Busenja_cm', palette='viridis')
plt.savefig('graph2_heatmap_depth.png')

# Graf 3: Metan (Pozitivno = Crveno, Negativno = Plavo)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT',
                hue='Metan_Senzor', palette={'Pozitivno': 'red', 'Negativno': 'blue'})
plt.savefig('graph3_methane_scatter.png')

# Graf 4: Kandidati (Velike crvene zvjezdice)
kandidati = df_cisto[(df_cisto['Metan_Senzor'] == 'Pozitivno') & (df_cisto['Organske_Molekule'] == 'Da')]
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', alpha=0.3, color='gray')
plt.scatter(kandidati['GPS_LONG'], kandidati['GPS_LAT'], marker='*', s=250, color='red', label='Kandidati')
plt.legend()
plt.savefig('scatter_plot.png')

# Graf 5: Satelitska snimka (jezero_mission_map.jpg)
plt.figure(figsize=(12, 8))
extent_koordinate = [df_cisto['GPS_LONG'].min(), df_cisto['GPS_LONG'].max(),
                     df_cisto['GPS_LAT'].min(), df_cisto['GPS_LAT'].max()]

try:
    # Učitavamo tvoju JPG sliku kao podlogu
    slika_kratera = plt.imread('jezero_crater_satellite_map.jpg')
    plt.imshow(slika_kratera, extent=extent_koordinate, aspect='auto', alpha=0.7)
    sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', alpha=0.3, color='white')
    plt.title("Navigacijska mapa: Krater Jezero")
    plt.savefig('jezero_mission_map.jpg')
    print("Graf 5 sa satelitskom snimkom je spreman!")
except:
    print(" Slika nije pronađena, graf 5 će biti bez podloge.")

print("Svi grafovi su uspješno generirani!")

print("Priprema JSON naloga za rover...")

lista_naloga = []

# Prolazimo kroz tablicu kandidata koju si već napravio u 4. grafu
for index, red in kandidati.iterrows():
    nalog = {
        "ID_Uzorka": int(red['ID_Uzorka']),
        "Koordinate": {
            "LAT": float(red['GPS_LAT']),
            "LONG": float(red['GPS_LONG'])
        },
        "Operacije": ["NAVIGACIJA", "SONDIRANJE", "SLANJE_PODATAKA"]
    }
    lista_naloga.append(nalog)

# --- 4. SLANJE PODATAKA ---
payload = {
    "ime": "Lino Lakača",
    "misija": "Nexus",
    "nalozi": lista_naloga
}

url_servera = "https://webhook.site/#!/view/03f33f00-c3a0-4a66-8b06-63f1af147efa"

try:
    odgovor = requests.post(url_servera, json=payload)

    if odgovor.status_code == 200:
        print("Misija Nexus uspješna! Rover je primio upute (Status 200).")
    else:
        print(f"Server je vratio status {odgovor.status_code}.")
        print(f"Poruka servera: {odgovor.text}")
except Exception as e:
    print(f"eza sa serverom nije uspostavljena: {e}")
