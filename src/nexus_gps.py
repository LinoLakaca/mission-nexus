import pandas as pd




df_gps = pd.read_csv("mars_sample_locations.csv", sep=';')

print("Prvih 5 redaka GPS podataka:")
print(df_gps.head())





df_kemija = pd.read_csv("mars_soil_samples.csv", sep=';')

print("\n=== Provjera integriteta ===")
print(f"Broj kemijskih uzoraka: {df_kemija.shape[0]}")
print(f"Broj GPS zapisa: {df_gps.shape[0]}")



min_lat = df_gps["GPS_LAT"].min()
max_lat = df_gps["GPS_LAT"].max()
min_long = df_gps["GPS_LONG"].min()
max_long = df_gps["GPS_LONG"].max()

print("\n=== Bounding Box (granice područja) ===")
print(f"Min Latitude: {min_lat}")
print(f"Max Latitude: {max_lat}")
print(f"Min Longitude: {min_long}")
print(f"Max Longitude: {max_long}")




povrsina = (max_lat - min_lat) * (max_long - min_long)
print(f"\nPovršina istraživanog pravokutnika (u stupnjevima): {povrsina}")