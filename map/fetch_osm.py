import json

import requests

OUT_JS = "points.js"
ENDPOINT = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"

VALUES = ["СДЭК", "СДЕК", "CDEK"]

QUERY = """
[out:json][timeout:300];
(
{nwr}
);
out center tags;
"""


def build_statements():
    lines = []
    for key in ("name", "brand"):
        for val in VALUES:
            lines.append(f'  nwr["{key}"="{val}"](41.0,19.0,82.0,180.0);')
            lines.append(f'  nwr["{key}"="{val}"](50.0,-180.0,71.0,-168.0);')
    return "\n".join(lines)


def main():
    q = QUERY.format(nwr=build_statements())
    r = requests.post(
        ENDPOINT,
        data={"data": q},
        headers={"User-Agent": "cdek-map/1.0 (pet project)"},
        timeout=320,
    )
    r.raise_for_status()
    data = r.json()

    seen = set()
    points = []
    for el in data.get("elements", []):
        oid = (el.get("type"), el.get("id"))
        if oid in seen:
            continue
        seen.add(oid)

        if el.get("type") == "node":
            lat, lon = el.get("lat"), el.get("lon")
        else:
            c = el.get("center")
            if not c:
                continue
            lat, lon = c.get("lat"), c.get("lon")

        if lat is None or lon is None:
            continue

        tags = el.get("tags") or {}
        name = (tags.get("name") or "").strip()
        phone = (tags.get("contact:phone") or "").strip()
        points.append([round(lon, 5), round(lat, 5), name, phone])

    js = "window.CDEK_POINTS = " + json.dumps(points, ensure_ascii=False) + ";\n"
    with open(OUT_JS, "w", encoding="utf-8") as f:
        f.write(js)

    print(f"found {len(points)} unique CDEK points -> {OUT_JS}")


if __name__ == "__main__":
    main()
