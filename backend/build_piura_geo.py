"""Build data/geo/piura_provinces.geojson: Piura region's 8 provinces for the start-screen map.

Source: pe-atlas 0.0.1 (MIT), districts-100k.json, a TopoJSON redistribution of the 2022 edition of
Peru's district boundary shapefiles published by GeoGPS Perú (INEI limits).
    https://www.npmjs.com/package/pe-atlas  ·  https://github.com/ccalobeto/pe-atlas

Provinces are the district boundaries merged: in the topology, a border shared by two districts of the
same province is internal and dropped; the borders left (used once) are stitched into the province outline.
Merging before simplifying keeps neighbouring provinces' shared borders identical.

Run from the Final Project folder (the raw download stays in data/raw/, which is not committed):
    curl -L -o data/raw/geo/pe-atlas-districts-100k.json https://unpkg.com/pe-atlas@0.0.1/districts-100k.json
    .venv\\Scripts\\python.exe -m backend.build_piura_geo
"""

import json
from collections import Counter

from backend import config

RAW = config.DATA_DIR / "raw" / "geo" / "pe-atlas-districts-100k.json"
OUT = config.DATA_DIR / "geo" / "piura_provinces.geojson"
PIURA_UBIGEO = "20"
# Province names by UBIGEO province code (INEI), Piura region.
PROVINCES = {"2001": "Piura", "2002": "Ayabaca", "2003": "Huancabamba", "2004": "Morropón", "2005": "Paita",
             "2006": "Sullana", "2007": "Talara", "2008": "Sechura"}
TOLERANCE = 0.0012   # degrees (~130 m)
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


def merge_rings(ring_arc_lists: list[list[int]], arcs: list) -> list[list[tuple[float, float]]]:
    """Dissolve districts into one outline: drop arcs used twice (internal borders), stitch the rest."""
    def base(i: int) -> int:
        return i if i >= 0 else ~i
    uses = Counter(base(i) for r in ring_arc_lists for i in r)
    segments = [arcs[i] if i >= 0 else arcs[~i][::-1] for r in ring_arc_lists for i in r if uses[base(i)] == 1]
    key = lambda p: (round(p[0], 9), round(p[1], 9))  # noqa: E731
    by_start: dict = {}
    for k, seg in enumerate(segments):
        by_start.setdefault(key(seg[0]), []).append(k)
    used = [False] * len(segments)
    rings = []
    for k, seg in enumerate(segments):
        if used[k]:
            continue
        used[k] = True
        pts, start = list(seg), key(seg[0])
        while key(pts[-1]) != start:
            nxt = next((j for j in by_start.get(key(pts[-1]), []) if not used[j]), None)
            if nxt is None:
                raise ValueError("open boundary while merging districts")
            used[nxt] = True
            pts.extend(segments[nxt][1:])
        rings.append(pts)
    return rings


def area(r: list) -> float:
    return sum(r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1] for i in range(len(r) - 1)) / 2


def inside(pt: tuple, r: list) -> bool:
    x, y = pt
    hit = False
    for i in range(len(r) - 1):
        (x1, y1), (x2, y2) = r[i], r[i + 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit


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


def build() -> dict:
    topo = json.loads(RAW.read_text(encoding="utf-8"))
    arcs = decode_arcs(topo)
    by_province: dict[str, list] = {}
    for g in topo["objects"]["districts"]["geometries"]:
        ubigeo = str(g["id"])
        if ubigeo.startswith(PIURA_UBIGEO):
            polys = [g["arcs"]] if g["type"] == "Polygon" else g["arcs"]
            by_province.setdefault(ubigeo[:4], []).extend(r for poly in polys for r in poly)
    features = []
    for code, ring_arcs in sorted(by_province.items()):
        rings = sorted(merge_rings(ring_arcs, arcs), key=lambda r: -abs(area(r)))
        polys: list[list] = []
        for r in rings:  # the largest rings are outlines; a ring inside one of them is a hole
            host = next((p for p in polys if inside(r[0], p[0])), None)
            (host.append(r) if host else polys.append([r]))
        coords = []
        for poly in polys:
            out = [[[round(x, DECIMALS), round(y, DECIMALS)] for x, y in simplify(r, TOLERANCE)] for r in poly]
            out = [r for r in out if len({tuple(p) for p in r}) >= 3]  # drop slivers
            if out:
                coords.append(out)
        features.append({"type": "Feature", "properties": {"ubigeo": code, "name": PROVINCES[code]},
                         "geometry": {"type": "MultiPolygon", "coordinates": coords}})
    return {"type": "FeatureCollection",
            "source": "pe-atlas 0.0.1 (MIT), districts-100k.json: GeoGPS Perú 2022 edition of INEI district limits, "
                      "merged into provinces",
            "source_url": "https://www.npmjs.com/package/pe-atlas", "features": features}


def main() -> None:
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    pts = sum(len(r) for f in data["features"] for p in f["geometry"]["coordinates"] for r in p)
    print(f"Wrote {OUT.relative_to(config.PROJECT_ROOT)}: {len(data['features'])} provinces, {pts} points, "
          f"{OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
