import pandas as pd

# Učitavanje podataka
df = pd.read_csv('mars_soil_samples.csv', sep=';')

print(f"Učitano uzoraka: {df.shape[0]}")

# Uzorak je OPASAN ako je pH < 3 ILI pH > 10
opasni_uzorci = df[
    (df['pH_Vrijednost'] < 3) |
    (df['pH_Vrijednost'] > 10)
]

print("\n--- OPASNE ZONE ---")
print(f"Pronađeno opasnih uzoraka: {opasni_uzorci.shape[0]}")

# Ispis prvih 5 opasnih uzoraka
print(opasni_uzorci.head())
