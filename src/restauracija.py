import pandas as pd
import requests
import json
import sys


df1 = pd.read_csv('ucenici.csv')
df2 = pd.read_csv('razredi.csv')

df_spojeno = pd.merge(
    df1,
    df2,
    left_on="razred_id",
    right_on="id"
)
print(df_spojeno)

ovo_sam_ja = df_spojeno[df_spojeno["id_x"]== 24]
print(ovo_sam_ja)

osoba = ovo_sam_ja.iloc[0]
print("----------------OSOBA----------------")
print(osoba)

json_osobni = {
    "podaci" : {
        "autor: ":"Lino Lakača",
        "ime": osoba["ime"],
        "prezime": osoba["prezime"],
        "razred": osoba["razred"],
        "smjer": osoba["smjer"]
    }
}
print("Pronađen učenik(JSON preview):")

def posalji_na_server(url, json_osobni):
    """
    Šalje podatke na centralni server koristeći POST metodu.
    """
    print(f"--- Šaljem podatke na: {url} ---")

    try:
        # timeout=5 znači: ako server šuti 5 sekundi, odustani.
        odgovor = requests.post(url, json=json_osobni, timeout=5)

        if odgovor.status_code == 200:
            print("SERVER POTVRDIO: Paket primljen.")
        else:
            print(f"SERVER ODBIO: Greška kod {odgovor.status_code}")

    except Exception as greska:
        print(f"KOMUNIKACIJSKA GREŠKA: {greska}")
server_url="https://webhook.site/e2ee3d3c-17a9-4e72-9356-1dd5a4406f13"
posalji_na_server(server_url, json_osobni)
tehnicari = df_spojeno[df_spojeno["smjer"] == "Tehničar za elektroniku"]
print(tehnicari)

broj_tehnicara = len(tehnicari)
print("Broj učenika:", broj_tehnicara)

popis = []

for i in range(len(tehnicari)):
    red = df_spojeno.iloc[i]

    ucenik = {
        "Ime": red["ime"],
        "Prezime": red["prezime"],
        "Razred": red["razred"]
    }

    popis.append(ucenik)

json_tehnicari = {
    "Autor": "Lino Lakača",
    "Smjer": "Tehničar za elektroniku",
    "Broj učenika": broj_tehnicara,
    "Popis": popis
}

print(json.dumps(json_tehnicari, indent=4, ensure_ascii=False))

posalji_na_server(server_url, json_tehnicari)
