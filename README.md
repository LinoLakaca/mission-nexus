# Projekt Nexus

## Ukratko o projektu

U ovom projektu radio sam analizu podataka za zamišljenu misiju rovera na Marsu, na području kratera Jezero. Podaci su zapisani u CSV datotekama i sadrže informacije o lokacijama uzoraka, temperaturi tla, dubini bušenja, pH vrijednosti, količini vode, metanu i organskim molekulama.

Cilj projekta bio je pronaći zanimljive lokacije koje bi rover trebao dodatno istražiti. Nakon obrade podataka napravio sam grafove, kartu i JSON nalog koji se može poslati kao uputa roveru.

## Struktura repozitorija

Repozitorij je podijeljen u nekoliko mapa:

```text
data/      - CSV datoteke s podacima
src/       - Python kodovi
assets/    - slike, grafovi i karta
README.md - opis projekta

U mapi data/ nalaze se CSV datoteke s podacima.
U mapi src/ nalaze se Python skripte koje sam koristio za generiranje, obradu i slanje podataka.
U mapi assets/ nalaze se slike grafova i karta koje su korištene u README dokumentu.

Obrada podataka

Podatke sam učitao pomoću biblioteke pandas. Prvo sam provjerio kako tablice izgledaju, koliko imaju redaka i stupaca te koje se vrijednosti nalaze u njima.

Nakon toga sam filtrirao podatke kako bih pronašao uzorke koji su najzanimljiviji za daljnju analizu. Gledao sam uzorke koji imaju bolju temperaturu tla, određenu količinu vode i pozitivan metanski senzor.

Primjer filtriranja kandidata:

kandidati = df[
    (df['Temp_Tla_C'] > -60) &
    (df['H2O_Postotak'] > 1.0) &
    (df['Metan_Senzor'] == 'Pozitivno')
]

Također sam uklonio očite greške u podacima, npr. nemoguće temperature ili neispravne pH vrijednosti. Takve vrijednosti mogu nastati zbog greške senzora i ne bi trebale utjecati na konačni rezultat.

Grafovi i analiza
Odnos temperature i vode

Ovaj graf prikazuje odnos između temperature tla i postotka vode u uzorcima. Točke su označene prema tome je li metanski senzor bio pozitivan ili negativan. Pozitivni metanski rezultati su važni jer mogu označavati zanimljiva mjesta za daljnje istraživanje.

Dubina bušenja

Ovdje se vidi raspored uzoraka prema GPS koordinatama. Boja prikazuje dubinu bušenja. Na taj način se može vidjeti gdje su uzorci uzimani i koliko duboko je rover bušio.

Kandidati za daljnje istraživanje

Na ovom grafu su posebno označene lokacije koje su odabrane kao kandidati. Crvene zvjezdice označavaju mjesta koja zadovoljavaju uvjete i koja bi rover trebao dodatno istražiti.

Karta kratera Jezero

Na ovoj slici su podaci prikazani na karti kratera Jezero. Za prikaz je korišten extent, što znači da su granice slike usklađene s najmanjim i najvećim GPS koordinatama iz podataka. Tako se točke mogu bolje prikazati na stvarnoj karti.

Metanski senzor

Ovaj graf prikazuje gdje se pojavljuju pozitivna i negativna očitanja metana. Pozitivna očitanja su korisna jer pomažu u odabiru lokacija koje imaju veći potencijal za istraživanje.

JSON Uplink

Nakon što su pronađeni kandidati, napravljen je JSON paket koji sadrži podatke za rover. U tom paketu nalaze se koordinate, ID uzorka i operacije koje rover treba napraviti.

Primjer JSON strukture:

{
    "misija": "NEXUS-UPLINK",
    "posiljatelj": "Lino Lakača",
    "broj_meta": 1,
    "meta": [
        {
            "sample_id": "101",
            "lokacija": {
                "lat": 18.48231,
                "lon": 77.39142
            },
            "status": "SPREMNO_ZA_SLANJE"
        }
    ]
}

Za izradu naloga koristio sam petlju, kako ne bih morao ručno pisati svaki uzorak. Program sam prolazi kroz sve kandidate i dodaje ih u listu naloga.

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
Problemi tijekom rada
Problem 1: Greške u podacima

U podacima su se pojavile neke vrijednosti koje nisu realne, npr. previsoka temperatura ili kriva pH vrijednost. To bi moglo pokvariti grafove i analizu.

Rješenje je bilo filtrirati takve podatke i izbaciti ih iz daljnje analize.

Problem 2: Spajanje tablica

Podaci o uzorcima i GPS lokacijama bili su u odvojenim CSV datotekama. Morao sam ih spojiti pomoću zajedničkog stupca ID_Uzorka.

df = pd.merge(df_gps, df_uzorci, on='ID_Uzorka')
Problem 3: Slanje na server

Kod slanja JSON paketa može doći do greške ako URL nije dobar ili ako server ne odgovara.

Zato sam koristio try-except, da program ne prestane raditi odmah nego da ispiše grešku.

try:
    odgovor = requests.post(url_servera, json=payload)
except Exception as e:
    print(f"Veza sa serverom nije uspostavljena: {e}")
Zaključak

Kroz ovaj projekt naučio sam kako se mogu obraditi CSV podaci pomoću Pythona, napraviti grafovi i izdvojiti najvažnije lokacije za rover. Također sam naučio kako se podaci mogu prikazati na karti i kako se može napraviti JSON nalog za slanje podataka. Projekt pokazuje kako se podaci mogu iskoristiti za donošenje odluka u robotskoj misiji.
