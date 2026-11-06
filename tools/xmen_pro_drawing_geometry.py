"""Reconcile exact Pro geometry with independently read Pro factory drawings.

The ordinary curator needs only the committed seed and standard library. Optional
image output verifies and annotates retained native composites; it never changes
the source render or derives a reading by inverting a desired table coordinate.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import drawing_callouts as callouts
from pinmame_game_defs.jsonio import file_sha256, load_json

SEED = "tools/seeds/stern/x-men-pro-2012-callouts.json"
SOURCE = "review.x-men-pro-drawing-reconciliation.20261106"


def rectify_quadrilateral(corners: list[list[float]], pixel: list[float]) -> tuple[float, float]:
    """Project a photographed part's four ordered corners onto its unit plane."""
    if len(corners) != 4:
        raise ValueError("a physical part plane needs four actual corners")
    matrix = []
    for (x,y),(u,v) in zip(corners, ((0,0),(1,0),(1,1),(0,1))):
        matrix.extend([[x,y,1,0,0,0,-u*x,-u*y,u], [0,0,0,x,y,1,-v*x,-v*y,v]])
    for column in range(8):
        pivot = max(range(column,8),key=lambda row:abs(matrix[row][column]))
        matrix[column],matrix[pivot] = matrix[pivot],matrix[column]
        divisor = matrix[column][column]
        if abs(divisor) < 1e-12:
            raise ValueError("degenerate physical part plane")
        matrix[column] = [value/divisor for value in matrix[column]]
        for row in range(8):
            if row != column:
                factor = matrix[row][column]
                matrix[row] = [value-factor*other for value,other in zip(matrix[row],matrix[column])]
    h = [row[8] for row in matrix]
    x,y=pixel
    divisor = h[6]*x+h[7]*y+1
    if abs(divisor) < 1e-12:
        raise ValueError("part-plane point is at infinity")
    result=((h[0]*x+h[1]*y+h[2])/divisor,(h[3]*x+h[4]*y+h[5])/divisor)
    if not all(math.isfinite(v) for v in result):
        raise ValueError("nonfinite physical part projection")
    return result


def validate_controls(seed: dict, objects: dict, position) -> None:
    if seed["machine_id"] != "stern.x-men-pro.2012" or seed["limit"] != callouts.LIMIT:
        raise ValueError("wrong machine or weakened drawing limit")
    if set(seed["pages"]) != {"switches", "coils", "lamps"}:
        raise ValueError("incomplete Pro drawing set")
    expected = {"Bumper2b", "Bumper1b", "Bumper3b", "LeftFlipper", "RightFlipper", "l3"}
    for key, page in seed["pages"].items():
        if len(page["controls"]) != 6 or {c["object"] for c in page["controls"]} != expected:
            raise ValueError(f"{key}: incomplete independent controls")
        pairs = []
        for control in page["controls"]:
            pixel=control["pixel"]
            if len(pixel)!=2 or not all(isinstance(v,(int,float)) and math.isfinite(v) and 0<=v<=page["image"][axis] for v,axis in zip(pixel,("width","height"))):
                raise ValueError(f"{key}: invalid native control pixel")
            x, y = position(objects[control["object"]])
            if control["xy"] != [x / 959, y / 2162]:
                raise ValueError(f"{key}: control differs from exact Pro object")
            pairs.append((control["pixel"], control["xy"]))
        span = max(xy[1] for _, xy in pairs) - min(xy[1] for _, xy in pairs)
        if span < callouts.MIN_CONTROL_SPAN or max(callouts.leave_one_out(pairs)) > callouts.LIMIT:
            raise ValueError(f"{key}: inadequate drawing calibration")


def inside_hull(point: list, controls: list[dict]) -> bool:
    """Include the boundary of the actual convex hull, not its bounding box."""
    points = sorted(set(tuple(c["pixel"]) for c in controls))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    halves = []
    for sequence in (points, list(reversed(points))):
        half = []
        for candidate in sequence:
            while len(half) >= 2 and cross(half[-2], half[-1], candidate) <= 0:
                half.pop()
            half.append(candidate)
        halves.append(half[:-1])
    hull = halves[0] + halves[1]
    return all(cross(hull[i], hull[(i + 1) % len(hull)], point) >= -1e-9 for i in range(len(hull)))


def add_measurements(definition: dict, seed: dict, manual_source: str) -> dict:
    devices = {d["id"]: d for d in definition["inputs"] + definition["outputs"]}
    report = {}
    for pid, measurement in seed["measurements"].items():
        device = devices[measurement["device_id"]]
        page = seed["pages"][measurement["page"]]
        x, y = callouts.measured(seed, pid)
        if not all(math.isfinite(value) and 0 <= value <= 1 for value in (x, y)):
            raise ValueError(f"{pid}: measured point outside the playfield")
        extrapolated = not inside_hull(measurement["pixel"], page["controls"])
        secondary = measurement.get("second_read")
        secondary_offset = None
        if secondary:
            if secondary["page"] == measurement["page"]:
                raise ValueError(f"{pid}: a measurement cannot corroborate itself")
            other = seed["pages"][secondary["page"]]
            transform = callouts.fit((c["pixel"], c["xy"]) for c in other["controls"])
            secondary_offset = callouts.distance((x, y), callouts.apply(transform, secondary["pixel"]))
            if secondary_offset > callouts.LIMIT:
                raise ValueError(f"{pid}: second Pro drawing disagrees")
        status = measurement["status"]
        if status not in {"observed", "validated"} or (status == "validated" and extrapolated and not secondary):
            raise ValueError(f"{pid}: unsupported measurement promotion")
        existing = device.get("spatial")
        if existing:
            if pid in {p["id"] for p in existing.get("placements", [])}:
                raise ValueError(f"{pid}: duplicate drawing measurement")
            census = seed.get("partial_censuses", {}).get(device["id"])
            partial = census and census["complete"] is False and pid in census["known_emitter_ids"] and "quantity" not in device["physical"]
            if not device.get("physical", {}).get("quantity", 0) > 1 and not partial:
                raise ValueError(f"{pid}: would silently add an emitter")
        if existing is None:
            device["spatial"] = {"status": status, "placements": []}
        device["spatial"]["placements"].append({
            "id": pid, "role": measurement["role"], "space": "playfield", "x": x, "y": y,
            "provenance": {"status": status, "source_refs": [manual_source, SOURCE, *measurement.get("source_refs", [])]},
        })
        device["spatial"]["status"] = min((p["provenance"]["status"] for p in device["spatial"]["placements"]), key={"observed": 0, "validated": 1}.__getitem__)
        device["physical"]["notes"] += " " + measurement["note"]
        report[pid] = {
            "page": measurement["page"], "pixel": measurement["pixel"], "normalized": [x, y],
            "point_type": measurement["point_type"], "uncertainty_px": measurement["uncertainty_px"],
            "extrapolated": extrapolated, "second_read": secondary,
            "second_drawing_offset": round(secondary_offset, 4) if secondary_offset is not None else None,
            "status": status,
        }
    # The rear photograph has two board-end controls and one observed edge axis.
    # That supplies coarse plan projections, not the four-control elevation check
    # required for validation. Refuse a status edit that would hide this limit.
    for pid, measurement in seed.get("elevation_measurements", {}).items():
        if measurement["status"] != "observed":
            raise ValueError("unresolved rear-photo perspective cannot be promoted")
        page = seed["elevations"][measurement["page"]]
        x, y = callouts.elevation_measured(seed, pid)
        if not 0 <= x <= 1 or not 0 <= y <= 1:
            raise ValueError("rear-panel projection outside playfield")
        device = devices[measurement["device_id"]]
        spatial = device.setdefault("spatial", {"status": "observed", "placements": []})
        if any(p["id"] == pid for p in spatial["placements"]):
            raise ValueError("duplicate rear emitter")
        spatial["placements"].append({"id":pid,"role":"emitter","space":"playfield","x":x,"y":y,"provenance":{"status":"observed","source_refs":[manual_source,SOURCE,"review.x-men-pro-gi-partial.20261106"]}})
        spatial["status"] = "observed"
        device["physical"]["notes"] += " " + measurement["note"]
        report[pid] = {"page":measurement["page"],"pixel":measurement["pixel"],"normalized":[x,y],"status":"observed","point_type":"rear_view_affine_panel_projection","controls":len(page["controls"]),"perspective_validated":False,"plane_y":page["plane_y"]}
    if mechanism := seed.get("trough_contact_projection"):
        page=seed["pages"][mechanism["target_page"]]
        transform=callouts.fit((c["pixel"],c["xy"]) for c in page["controls"])
        exit_pixel,entry_pixel=mechanism["target_axis"]
        if [p["address"] for p in mechanism["contacts"]] != [18,19,20]:
            raise ValueError("incomplete or reordered mechanical trough contacts")
        fractions=[]
        for measurement in mechanism["contacts"]:
            if measurement["status"] != "observed":
                raise ValueError("raised contact tips are outside the rectified plate plane; projection stays observed")
            fraction,cross=rectify_quadrilateral(mechanism["photo_corners"],measurement["pixel"])
            if not 0 < fraction < 1:
                raise ValueError("trough contact outside its own guideplate length")
            fractions.append(fraction)
            target=[a+(b-a)*fraction for a,b in zip(exit_pixel,entry_pixel)]
            xy=tuple(round(v,3) for v in callouts.apply(transform,target))
            if list(xy) != measurement["normalized"] or not all(0<=v<=1 for v in xy):
                raise ValueError("trough contact projection does not reproduce")
            device=devices[measurement["device_id"]]
            if device.get("spatial"):
                raise ValueError("trough projection would overwrite source geometry")
            pid=device["id"]+".sensor"
            device["spatial"]={"status":"observed","placements":[{"id":pid,"role":"sensor","space":"playfield","x":xy[0],"y":xy[1],"provenance":{"status":"observed","source_refs":[manual_source,SOURCE,"review.x-men-pro-trough-contact-projection.20261106"]}}]}
            device.setdefault("physical",{})["notes"]="Own-contact longitudinal projection from photographed500-6318-24-ND guideplate onto actual Pro diagonal trough. Each of three actuator-tip pixels is rectified separately, not equally spaced or copied from LE. Raised tips lie outside the guideplate plane, so residual parallax is unresolved and these points remain observed; they are not precise ball-contact centers."
            report[pid]={"point_type":"own_contact_longitudinal_projection","photo_pixel":measurement["pixel"],"unit_fraction":round(fraction,6),"cross_plane_coordinate":round(cross,6),"target_pixel":[round(v,3) for v in target],"normalized":list(xy),"status":"observed","coplanarity_validated":False}
        if not fractions[0]>fractions[1]>fractions[2]:
            raise ValueError("mechanical trough ordering reversed")
    for pid, measurement in seed.get("local_photo_measurements", {}).items():
        # This is one bounded local assembly projection, not a whole-playfield
        # drawing check. Its target must be inside actual source controls.
        controls=measurement["controls"]
        if len(controls)<6 or len({c["lamp"] for c in controls})!=len(controls):
            raise ValueError("local photo needs six distinct independent controls")
        lamps={d["binding"]["device"]:d for d in definition["outputs"] if d["binding"]["group"]=="pinmame.output.lamp"}
        for control in controls:
            placement=lamps[control["lamp"]]["spatial"]["placements"][0]
            if [placement["x"],placement["y"]]!=control["xy"] or placement["id"] not in seed["checks"]:
                raise ValueError("local photo control is not independently reconciled")
        pairs=[(c["pixel"],c["xy"]) for c in controls]
        offsets=callouts.leave_one_out(pairs)
        if max(offsets)>callouts.LIMIT or not inside_hull(measurement["pixel"],controls):
            raise ValueError("local photo extrapolation or inadequate independent fit")
        transform=callouts.fit(pairs)
        xy=tuple(round(v,3) for v in callouts.apply(transform,measurement["pixel"]))
        if list(xy)!=measurement["normalized"] or not all(0<=v<=1 for v in xy):
            raise ValueError("local photo measurement does not reproduce")
        device=devices[measurement["device_id"]]
        if device.get("spatial") or device["physical"]["quantity"]!=1:
            raise ValueError("local photo would duplicate or omit an emitter")
        device["spatial"]={"status":"validated","placements":[{"id":pid,"role":"emitter","space":"playfield","x":xy[0],"y":xy[1],"provenance":{"status":"validated","source_refs":[manual_source,SOURCE,"review.x-men-pro-local-spotlight.20261106"]}}]}
        device["physical"]["notes"]+=" "+measurement["note"]
        head=callouts.apply(transform,measurement["head_pixel"])
        report[pid]={"point_type":"bounded_local_photo_own_housing_projection","pixel":measurement["pixel"],"normalized":list(xy),"controls":len(controls),"control_loo_max":round(max(offsets),6),"inside_control_hull":True,"head_pixel":measurement["head_pixel"],"visible_head_to_mount_offset":round(callouts.distance(xy,head),6),"height_parallax":"Not independently measured. The own housing-head mounting-foot projection is explicit; no hidden filament precision is asserted.","status":"validated"}
    for device in devices.values():
        spatial = device.get("spatial", {})
        if spatial.get("placements") and device.get("physical", {}).get("quantity"):
            if len(spatial["placements"]) != device["physical"]["quantity"]:
                raise ValueError(f"{device['id']}: incomplete physical emitter measurements")
    for device_id, census in seed.get("partial_censuses", {}).items():
        device = devices[device_id]
        if census["complete"] is not False or "quantity" in device["physical"] or set(census["known_emitter_ids"]) != {p["id"] for p in device["spatial"]["placements"]}:
            raise ValueError("a partial census cannot assert whole-device quantity or omit known emitters")
        device["spatial"]["status"] = "observed"
    return report


def annotate(seed: dict, definition: dict, manuals: Path, output: Path, review_artifacts: Path | None = None) -> None:
    from PIL import Image, ImageDraw

    if output.exists():
        raise ValueError("retain prior overlays; choose a fresh successor directory")
    output.mkdir(parents=True)
    placements = callouts.placements_of(definition)
    for key, page in seed["pages"].items():
        source = manuals / page["image"]["path"]
        if file_sha256(source) != page["image"]["sha256"]:
            raise ValueError(f"wrong native source image {key}")
        image = Image.open(source).convert("RGB")
        draw = ImageDraw.Draw(image)
        for read in page["reads"]:
            x, y = read["pixel"]
            draw.ellipse((x-10, y-10, x+10, y+10), outline="red", width=3)
            draw.text((x+12, y-12), read["label"], fill="red")
        for control in page["controls"]:
            x, y = control["pixel"]
            draw.rectangle((x-10, y-10, x+10, y+10), outline="blue", width=3)
            draw.text((x+12, y+12), control["object"], fill="blue")
        for pid, measurement in seed["measurements"].items():
            if measurement["page"] == key:
                x, y = measurement["pixel"]
                draw.ellipse((x-16,y-16,x+16,y+16),outline="magenta",width=3)
                draw.text((x+18,y+16),pid,fill="magenta")
        transform = callouts.fit((c["pixel"], c["xy"]) for c in page["controls"])
        (a, b, c), (d, e, f) = transform
        for pid, check in seed["checks"].items():
            if check["page"] != key:
                continue
            px, py = placements[pid]
            x = ((px-c)*e - b*(py-f)) / (a*e-b*d)
            y = (a*(py-f) - d*(px-c)) / (a*e-b*d)
            draw.line((x-12, y, x+12, y), fill="green", width=3)
            draw.line((x, y-12, x, y+12), fill="green", width=3)
        mechanism=seed.get("trough_contact_projection")
        if mechanism and mechanism["target_page"]==key:
            start,end=mechanism["target_axis"]
            draw.line((*start,*end),fill="cyan",width=4)
            for contact in mechanism["contacts"]:
                fraction,_=rectify_quadrilateral(mechanism["photo_corners"],contact["pixel"])
                x,y=[a+(b-a)*fraction for a,b in zip(start,end)]
                draw.ellipse((x-12,y-12,x+12,y+12),outline="red",width=3)
                draw.text((x+15,y),str(contact["address"]),fill="red")
        image.save(output / f"{key}-overlay.png")
    for key, page in seed.get("elevations", {}).items():
        if review_artifacts is None:
            raise ValueError("rear-photo overlay requires --review-artifacts")
        source = review_artifacts / page["image"]["path"]
        if file_sha256(source) != page["image"]["sha256"]:
            raise ValueError("wrong rear photo for overlay")
        image = Image.open(source).convert("RGB")
        draw = ImageDraw.Draw(image)
        for control in page["controls"]:
            x,y=control["pixel"]
            draw.ellipse((x-8,y-8,x+8,y+8),outline="blue",width=3)
        for pid, measurement in seed.get("elevation_measurements", {}).items():
            if measurement["page"] != key:continue
            x,y=measurement["pixel"]
            draw.ellipse((x-10,y-10,x+10,y+10),outline="red",width=3)
            draw.text((x-30,y+12),pid.split(".emitter.")[-1],fill="red")
        image.save(output/f"{key}-overlay.png")
    if review_artifacts is not None:
        for measurement in seed.get("local_photo_measurements",{}).values():
            source=review_artifacts/measurement["image"]["path"]
            if file_sha256(source)!=measurement["image"]["sha256"]:
                raise ValueError("wrong local photo overlay source")
            image=Image.open(source).convert("RGB");draw=ImageDraw.Draw(image)
            for control in measurement["controls"]:
                x,y=control["pixel"]
                draw.ellipse((x-12,y-12,x+12,y+12),outline="blue",width=4)
                draw.text((x+15,y),str(control["lamp"]),fill="blue")
            for label,point,color in (("head",measurement["head_pixel"],"red"),("own mount projection",measurement["pixel"],"magenta")):
                x,y=point;draw.ellipse((x-12,y-12,x+12,y+12),outline=color,width=4);draw.text((x+15,y),label,fill=color)
            image.crop((600,1000,2320,1500)).save(output/"local-spotlight-overlay.png")
        mechanism=seed.get("trough_contact_projection")
        if mechanism:
            source=review_artifacts/"stern/x-men-pro-2012/session-20261106"/mechanism["source_photo"]["path"]
            if file_sha256(source)!=mechanism["source_photo"]["sha256"]:
                raise ValueError("wrong component photo overlay source")
            image=Image.open(source).convert("RGB");draw=ImageDraw.Draw(image)
            for index,(x,y) in enumerate(mechanism["photo_corners"]):
                draw.ellipse((x-5,y-5,x+5,y+5),outline="blue",width=2);draw.text((x+6,y),str(index),fill="blue")
            for contact in mechanism["contacts"]:
                x,y=contact["pixel"];draw.ellipse((x-5,y-5,x+5,y+5),outline="red",width=2);draw.text((x+6,y),str(contact["address"]),fill="red")
            image.save(output/"trough-contact-photo-overlay.png")


def render_excerpts(seed: dict, manuals: Path, repository: Path, review_artifacts: Path | None = None) -> None:
    """Crop the pinned full native composites without resampling their pixels."""
    import PIL
    from PIL import Image

    crops = {"switches": (40, 280, 1410, 3260), "coils": (120, 300, 1500, 3270), "lamps": (80, 280, 1450, 3270)}
    import json
    records = {}
    for key, box in crops.items():
        source = seed["pages"][key]["image"]
        image = manuals / source["path"]
        if file_sha256(image) != source["sha256"]:
            raise ValueError(f"wrong native image {key}")
        relative = f"evidence/excerpts/stern.x-men-pro.2012/pro-{key}-locations.webp"
        destination = repository / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        Image.open(image).convert("L").crop(box).save(destination, format="WEBP", quality=80, method=6)
        records[key] = {
            "image": relative, "image_sha256": file_sha256(destination),
            "image_derivation": f"Native2550x3300 composite SHA256 {source['sha256']}; 300dpi derived from source stencil matrix axes, not assumed. Exact native pixel crop {box}, no resize; tools/xmen_pro_drawing_geometry.py, Pillow{PIL.__version__}, grayscale WebP quality80 method6.",
        }
    if review_artifacts is not None:
        photo = seed["elevations"]["pro-factory-rear"]["image"]
        source = review_artifacts / photo["path"]
        if file_sha256(source) != photo["sha256"]:
            raise ValueError("wrong native Pro factory photograph crop")
        relative = "evidence/excerpts/stern.x-men-pro.2012/pro-factory-backpanel.webp"
        Image.open(source).convert("L").save(repository/relative,format="WEBP",quality=80,method=6)
        records["rear-photo"]={"image":relative,"image_sha256":file_sha256(repository/relative),"image_derivation":f"Michael Minn4320x3240 photograph, native crop(550,1310,1670,1830),1120x520, no resize or assumed DPI. Native crop SHA256{photo['sha256']}; tools/xmen_pro_drawing_geometry.py, Pillow{PIL.__version__}, grayscale WebP quality80 method6."}
        for measurement in seed.get("local_photo_measurements",{}).values():
            photo=measurement["image"]
            source=review_artifacts/photo["path"]
            if file_sha256(source)!=photo["sha256"]:
                raise ValueError("wrong local Pro photo")
            relative="evidence/excerpts/stern.x-men-pro.2012/pro-spotlight-local.webp"
            Image.open(source).convert("L").crop((1050,1060,1330,1320)).save(repository/relative,format="WEBP",quality=80,method=6)
            records["spotlight-local"]={"image":relative,"image_sha256":file_sha256(repository/relative),"image_derivation":f"Native3000x2000 actual Pro photo SHA256{photo['sha256']}; native crop(1050,1060,1330,1320),280x260,no resize or assumed DPI. Pillow{PIL.__version__},grayscale WebP quality80 method6,tools/xmen_pro_drawing_geometry.py. Tight own-fixture reading aid; complete control overlay stays external."}
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manuals", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--render-excerpts", action="store_true")
    parser.add_argument("--review-artifacts", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    seed = load_json(root / SEED)
    if args.render_excerpts:
        render_excerpts(seed, args.manuals, root, args.review_artifacts)
    if args.output:
        from curate_xmen_pro_spatial import build
        annotate(seed, build(root)[0], args.manuals, args.output, args.review_artifacts)
    elif not args.render_excerpts:
        parser.error("provide --output or --render-excerpts")
