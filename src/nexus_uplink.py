import csv
import json
import datetime
import requests


SOIL_SAMPLES_CSV = "mars_soil_samples.csv"
LOCATIONS_CSV = "mars_sample_locations.csv"
OUTPUT_JSON = "uplink_payload.json"

STUDENT_NAME = "Lino Lakača"

SERVER_URL = "https://webhook.site/f79bf0fc-e5b4-4f0e-a5d2-023d21e0403d"


def read_csv_dicts(path):

    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def filter_candidates(samples_rows):

    kandidati = []

    for r in samples_rows:
        try:
            h2o = float(str(r.get("H2O_Postotak", "0")).replace(",", ".").strip())
            organske = str(r.get("Organske_Molekule", "")).strip().lower()

            if h2o > 0 and organske in ("da", "yes", "true", "1"):
                kandidati.append(r)

        except Exception:
            continue

    return kandidati


def build_location_index(loc_rows):
    idx = {}

    for r in loc_rows:
        sid = str(r.get("ID_Uzorka", "")).strip()
        if not sid:
            continue

        lat = float(str(r.get("GPS_LAT", "")).replace(",", ".").strip())
        lon = float(str(r.get("GPS_LONG", "")).replace(",", ".").strip())

        idx[sid] = {"lat": lat, "lon": lon}

    return idx


def build_payload(student_name, candidate_rows, loc_index):
    timestamp = str(datetime.datetime.now())

    meta = []
    missing = []

    for r in candidate_rows:
        sid = str(r.get("ID_Uzorka", "")).strip()
        if not sid:
            continue

        if sid not in loc_index:
            missing.append(sid)
            continue

        kemija = {k: v for k, v in r.items() if v not in (None, "", " ")}

        meta.append({
            "sample_id": sid,
            "lokacija": {
                "lat": loc_index[sid]["lat"],
                "lon": loc_index[sid]["lon"]
            },
            "kemija": kemija
        })

    payload = {
        "misija": "NEXUS-UPLINK",
        "posiljatelj": student_name,
        "vrijeme": timestamp,
        "broj_meta": len(meta),
        "meta": meta,
        "status": "SPREMNO_ZA_SLANJE"
    }

    return payload, missing


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def send_to_server(url, payload):
    print(f"--- Šaljem podatke na: {url} ---")
    try:
        resp = requests.post(url, json=payload, timeout=5)

        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print("SERVER POTVRDIO: Paket primljen.")
        else:
            print("SERVER ODBIO zahtjev.")

        try:
            print("Odgovor servera:", resp.json())
        except Exception:
            print("Odgovor servera (text):", resp.text[:300])

    except Exception as e:
        print(f"KOMUNIKACIJSKA GREŠKA: {e}")


def main():
    soil_samples = read_csv_dicts(SOIL_SAMPLES_CSV)
    locations = read_csv_dicts(LOCATIONS_CSV)

    if not soil_samples:
        print("Greška: mars_soil_samples.csv je prazan ili se ne može učitati.")
        return

    if not locations:
        print("Greška: mars_sample_locations.csv je prazan ili se ne može učitati.")
        return

    candidates = filter_candidates(soil_samples)
    loc_index = build_location_index(locations)

    payload, missing_ids = build_payload(STUDENT_NAME, candidates, loc_index)

    print(f"Ukupno uzoraka tla: {len(soil_samples)}")
    print(f"Kandidata (po kemiji): {len(candidates)}")
    print(f"Meta s pronađenom lokacijom: {payload['broj_meta']}")

    if missing_ids:
        print("UPOZORENJE: Kandidati bez lokacije:", missing_ids)

    save_json(OUTPUT_JSON, payload)
    print(f"JSON spremljen u: {OUTPUT_JSON}")

    if not SERVER_URL.startswith("https://"):
        print("SERVER_URL nije https:// — provjeri URL s projektora.")
        return

    send_to_server(SERVER_URL, payload)

if __name__ == "__main__":
    main()
