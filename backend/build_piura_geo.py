"""Build data/geo/piura_districts.geojson: Piura region's district boundaries for the start-screen map.

Source: pe-atlas 0.0.1 (MIT), districts-100k.json, a TopoJSON redistribution of the 2022 edition of
Peru's district boundary shapefiles published by GeoGPS Perú (INEI limits).
    https://www.npmjs.com/package/pe-atlas  ·  https://github.com/ccalobeto/pe-atlas

Run from the Final Project folder (the raw download stays in data/raw/, which is not committed):
    curl -L -o data/raw/geo/pe-atlas-districts-100k.json https://unpkg.com/pe-atlas@0.0.1/districts-100k.json
    .venv\\Scripts\\python.exe -m backend.build_piura_geo
"""

import json

from backend import config

RAW = config.DATA_DIR / "raw" / "geo" / "pe-atlas-districts-100k.json"
OUT = config.DATA_DIR / "geo" / "piura_districts.geojson"
PIURA_UBIGEO = "20"
# Province names by UBIGEO province code (INEI), Piura region.
PROVINCES = {"2001": "Piura", "2002": "Ayabaca", "2003": "Huancabamba", "2004": "Morropón", "2005": "Paita",
             "2006": "Sullana", "2007": "Talara", "2008": "Sechura"}
TOLERANCE = 0.0008   # degrees (~90 m): keeps small districts' shapes, drops redundant points
DECIMALS = 4         # ~11 m


def decode_arcs(topo: dict) -> list[list[tuple[float, float]]]:
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:  # delta-encoded, quantized
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    return arcs


def ring(indexes: list[int], arcs: list) -> list[tuple[float, float]]:
    pts = []
    for i in indexes:
        seg = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(seg if not pts else seg[1:])
    return pts


def simplify(pts: list, tol: float) -> list:
    """Douglas-Peucker on one closed ring (keeps first/last point)."""
    if len(pts) < 5:
        return pts

    def dp(a: int, b: int, keep: set):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        norm = (dx * dx + dy * dy) ** 0.5 or 1e-12
        best, idx = 0.0, None
        for i in range(a + 1, b):
            d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / norm
            if d > best:
                best, idx = d, i
        if idx is not None and best > tol:
            keep.add(idx)
            dp(a, idx, keep)
            dp(idx, b, keep)

    mid = len(pts) // 2  # split a closed ring in two so the end points are not the same point
    keep = {0, mid, len(pts) - 1}
    dp(0, mid, keep)
    dp(mid, len(pts) - 1, keep)
    out = [pts[i] for i in sorted(keep)]
    return out if len(out) >= 4 else pts


def fix_name(name: str) -> str:
    """The TopoJSON stores some names double-encoded through Windows-1252 (e.g. "PARIÃ‘AS" for "PARIÑAS")."""
    try:
        return name.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name


def build() -> dict:
    topo = json.loads(RAW.read_text(encoding="utf-8"))
    arcs = decode_arcs(topo)
    features = []
    for g in topo["objects"]["districts"]["geometries"]:
        ubigeo = str(g["id"])
        if not ubigeo.startswith(PIURA_UBIGEO):
            continue
        polys = [g["arcs"]] if g["type"] == "Polygon" else g["arcs"]
        coords = []
        for poly in polys:
            rings = [[[round(x, DECIMALS), round(y, DECIMALS)] for x, y in simplify(ring(r, arcs), TOLERANCE)] for r in poly]
            solid = lambda r: len({tuple(p) for p in r}) >= 3  # noqa: E731 (fewer distinct points = a sliver)
            if solid(rings[0]):  # skip a polygon whose outer ring is a sliver; drop sliver holes
                coords.append([rings[0]] + [r for r in rings[1:] if solid(r)])
        features.append({"type": "Feature",
                         "properties": {"ubigeo": ubigeo, "name": fix_name(g["properties"]["name"]),
                                        "province": PROVINCES.get(ubigeo[:4], "")},
                         "geometry": {"type": "MultiPolygon", "coordinates": coords}})
    features.sort(key=lambda f: f["properties"]["ubigeo"])
    return {"type": "FeatureCollection",
            "source": "pe-atlas 0.0.1 (MIT), districts-100k.json: GeoGPS Perú 2022 edition of INEI district limits",
            "source_url": "https://www.npmjs.com/package/pe-atlas", "features": features}


def main() -> None:
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    pts = sum(len(r) for f in data["features"] for p in f["geometry"]["coordinates"] for r in p)
    print(f"Wrote {OUT.relative_to(config.PROJECT_ROOT)}: {len(data['features'])} districts, {pts} points, "
          f"{OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
