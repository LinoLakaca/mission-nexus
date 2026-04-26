import pandas as pd

print("Sustav za analizu podataka inicijaliziran...")

# Pokušaj učitavanja
df = pd.read_csv('mars_soil_samples.csv', sep=';')

# ispis prvih 5 redaka (OBAVEZNO koristiti print)
print("---POKUŠAJ 1 ---")
print(df.head(10))

print("\n--- STRUKTURA PODATAKA ---")
df.info()



print("\n--- STRUKTURA PODATAKA (ALTERNATIVA) ---")
# 1. Broj redaka i stupaca
print(f"Dimenzije tablice: {df.shape}")
# 2. Tipovi podataka po stupcima
print("\nTipovi podataka:")
print(df.dtypes)




print("\n--- STATISTIKA MARSA (RUČNO) ---")
# 1. Temperatura
print(f"Najniža temperatura: {df['Temp_Tla_C'].min()} C")
print(f"Najviša temperatura: {df['Temp_Tla_C'].max()} C")
# 2. pH Vrijednost (Prosjek)
print(f"Prosječni pH: {df['pH_Vrijednost'].mean()}")
# 3. Voda (Maksimum)
print(f"Maksimalni postotak vode: {df['H2O_Postotak'].max()} %")







