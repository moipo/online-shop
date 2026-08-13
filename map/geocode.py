import json
import re
import sys
import time

import requests
from openpyxl import load_workbook

XLSX = "cdek_PVZ.xlsx"
OUT_JS = "points.js"

UA = "CDEK-PVZ-Geocoder/1.0"
BASE = "https://nominatim.openstreetmap.org/search"

SAVE_EVERY = 20
SLEEP = 1.05

COL_LAT = 6
COL_LNG = 7
COL_CITY = 2
COL_ADDR = 3


def clean(s):
    if s is None:
        return ""
    s = str(s).strip()
    s = re.sub(r"\s+", " ", s)
    return s.strip(" ,.")


def strip_house(address):
    parts = [p.strip() for p in re.split(r"[,]", address) if p.strip()]
    kept = [p for p in parts if not re.search(r"\d", p)]
    return ", ".join(kept) if kept else ""


def build_queries(city, address):
    city = clean(city)
    address = clean(address)
    queries = []
    if city and address:
        queries.append(f"Россия, {city}, {address}")
        street = strip_house(address)
        if street and street != address:
            queries.append(f"Россия, {city}, {street}")
        queries.append(f"{city}, {address}")
    if city:
        queries.append(f"Россия, {city}")
        queries.append(city)
    elif address:
        queries.append(f"Россия, {address}")
        queries.append(address)
    seen = set()
    out = []
    for q in queries:
        if q not in seen:
            seen.add(q)
            out.append(q)
    return out


def in_russia(lat, lon):
    return (40.0 <= lat <= 85.0) and (lon >= 19.0 or lon <= -168.0)


def acceptable(result):
    if not result:
        return False
    try:
        lat = float(result.get("lat"))
        lon = float(result.get("lon"))
    except (TypeError, ValueError):
        return False
    cc = (result.get("address") or {}).get("country_code")
    if cc in ("ru", "ua"):
        return True
    return in_russia(lat, lon)


def geocode(query, session):
    params = {
        "q": query,
        "format": "jsonv2",
        "limit": 1,
        "accept-language": "ru",
        "addressdetails": 1,
    }
    headers = {"User-Agent": UA}
    for attempt in range(3):
        time.sleep(SLEEP)
        try:
            r = session.get(BASE, params=params, headers=headers, timeout=30)
        except requests.RequestException as exc:
            print(f"    [network error] {exc}", flush=True)
            time.sleep(2 ** attempt * 5)
            continue

        if r.status_code == 200:
            try:
                data = r.json()
            except ValueError:
                return None
            if data:
                return data[0]
            return None
        if r.status_code in (429, 500, 502, 503, 504):
            print(f"    [HTTP {r.status_code}] backoff, retry {attempt+1}", flush=True)
            time.sleep(2 ** attempt * 5)
            continue
        return None
    return None


def resolve(city, address, session):
    queries = build_queries(city, address)
    for i, q in enumerate(queries):
        result = geocode(q, session)
        if acceptable(result):
            return result, i
    return None, -1


def generate_points_js(ws):
    points = []
    for r in range(2, ws.max_row + 1):
        lat = ws.cell(r, COL_LAT).value
        lng = ws.cell(r, COL_LNG).value
        city = clean(ws.cell(r, COL_CITY).value)
        address = clean(ws.cell(r, COL_ADDR).value)
        if lat is None or lng is None:
            continue
        if lat == "NULL" or lng == "NULL":
            continue
        try:
            lat = float(lat)
            lng = float(lng)
        except (TypeError, ValueError):
            continue
        points.append(
            {
                "id": r - 1,
                "region": city,
                "address": address,
                "coordinates": [round(lng, 6), round(lat, 6)],
            }
        )
    js = "window.CDEK_POINTS = " + json.dumps(points, ensure_ascii=False) + ";\n"
    with open(OUT_JS, "w", encoding="utf-8") as f:
        f.write(js)
    return len(points)


def main():
    wb = load_workbook(XLSX)
    ws = wb.active

    if ws.cell(1, COL_LAT).value is None:
        ws.cell(1, COL_LAT).value = "Широта"
    if ws.cell(1, COL_LNG).value is None:
        ws.cell(1, COL_LNG).value = "Долгота"

    total = ws.max_row - 1
    session = requests.Session()

    done = 0
    success = 0
    nulls = 0
    exact = 0
    street_level = 0
    city_level = 0
    skipped = 0

    for r in range(2, ws.max_row + 1):
        lat_cell = ws.cell(r, COL_LAT)
        lng_cell = ws.cell(r, COL_LNG)
        if lat_cell.value is not None or lng_cell.value is not None:
            skipped += 1
            continue

        city = ws.cell(r, COL_CITY).value
        address = ws.cell(r, COL_ADDR).value

        result, level = resolve(city, address, session)
        if result:
            lat_cell.value = float(result["lat"])
            lng_cell.value = float(result["lon"])
            success += 1
            if level == 0:
                exact += 1
            elif level == 1:
                street_level += 1
            else:
                city_level += 1
        else:
            lat_cell.value = "NULL"
            lng_cell.value = "NULL"
            nulls += 1

        done += 1
        if done % SAVE_EVERY == 0:
            wb.save(XLSX)
            print(
                f"[progress] processed={done} exact={exact} street={street_level} "
                f"city={city_level} NULL={nulls} skipped_before={skipped}",
                flush=True,
            )

    wb.save(XLSX)
    n_points = generate_points_js(ws)
    print(
        f"[done] processed={done} exact={exact} street={street_level} "
        f"city={city_level} NULL={nulls} skipped_before={skipped} "
        f"points_written={n_points}",
        flush=True,
    )


if __name__ == "__main__":
    main()
